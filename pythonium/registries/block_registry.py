import contextlib
import json
from pathlib import Path
from typing import Any

BLOCK_PATH = Path(__file__).parent / "block.json"


class BlockRegistry:
    """Class for managing block registry."""

    __slots__ = ("_registry",)

    def __init__(self) -> None:
        self._registry: dict[
            str, tuple[int, dict[str, tuple[list[str], int]]]
        ] = {}
        self._load_registry()

    def _load_registry(self) -> None:
        with BLOCK_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)

        for block in data:
            name = f"minecraft:{block['name']}"
            min_id = block["minStateId"]
            states = block.get("states", [])

            weights: list[int] = []
            current_weight = 1
            for state in reversed(states):
                weights.insert(0, current_weight)
                current_weight *= state["num_values"]

            block_props = {}
            for i, state in enumerate(states):
                p_name = state["name"]

                if state["type"] == "bool":
                    values = ["true", "false"]
                else:
                    values = state.get("values", [])

                block_props[p_name] = (values, weights[i])

            self._registry[name] = (min_id, block_props)

    def get_id(self, name: str, **kwargs: Any) -> int:  # noqa: ANN401
        if ":" not in name:
            name = f"minecraft:{name}"

        res = self._registry.get(name)
        if not res:
            return 0

        min_id, props = res
        offset = 0

        for p_name, (values, weight) in props.items():
            val = kwargs.get(p_name)
            if val is not None:
                val_str = str(val).lower()
                with contextlib.suppress(ValueError):
                    offset += values.index(val_str) * weight

        return min_id + offset


BLOCK_REGISTRY = BlockRegistry()
