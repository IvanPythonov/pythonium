import itertools
import json
from pathlib import Path
from typing import Self

from pythonium.registries.base import Registry

type BlockProperty = str | bool
type BlockStateId = int


class BlockRegistry(Registry[BlockStateId]):
    """Block registry."""

    __registry_path__ = Path(__file__).parent / "block.json"

    def __init__(self) -> None:
        super().__init__()
        self.id_to_item_id: dict[int, int] = {}
        self.name_to_default_id: dict[str, int] = {}

    def discover(self) -> Self:
        with self.__registry_path__.open(encoding="utf-8") as f:
            blocks_data: list[dict] = json.load(f)

        for block in blocks_data:
            block_name = f"minecraft:{block['name']}"
            states = block.get("states", [])
            min_state_id = block["minStateId"]

            self.name_to_default_id[block_name] = block.get(
                "defaultState",
                min_state_id,
            )

            sorted_states = sorted(states, key=lambda s: s["name"])
            property_names = [state["name"] for state in sorted_states]

            property_values: list[list[str]] = []
            for state in sorted_states:
                if state["type"] == "bool":
                    property_values.append(["true", "false"])
                else:
                    property_values.append(state["values"])

            combinations = (
                itertools.product(*property_values)
                if property_values
                else [()]
            )

            for combination in combinations:
                if property_names:
                    properties = ",".join(
                        f"{name}={value}"
                        for name, value in zip(
                            property_names,
                            combination,
                            strict=False,
                        )
                    )
                    key = f"{block_name}[{properties}]"
                else:
                    key = block_name

                offset = 0
                multiplier = 1

                for state in reversed(sorted_states):
                    values = (
                        ["true", "false"]
                        if state["type"] == "bool"
                        else state["values"]
                    )

                    value = combination[property_names.index(state["name"])]
                    offset += values.index(value) * multiplier
                    multiplier *= len(values)

                state_id = min_state_id + offset

                self.register(key, state_id)

                drops = block.get("drops")
                if drops:
                    self.id_to_item_id[state_id] = drops[0]

        return self

    def get_drop_for_state(self, state_id: int) -> int:
        return self.id_to_item_id.get(state_id, 0)

    def get_id(
        self,
        name: str,
        **properties: BlockProperty,
    ) -> int:
        if ":" not in name:
            name = f"minecraft:{name}"

        if not properties:
            return self.name_to_default_id.get(name, 0)

        props = ",".join(
            f"{key}={str(value).lower()}"
            for key, value in sorted(properties.items())
        )

        return self.get(f"{name}[{props}]")


BLOCK_REGISTRY = BlockRegistry().discover()
