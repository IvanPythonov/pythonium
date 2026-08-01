import json
from pathlib import Path
from typing import Self

from pythonium.engine.enums import Direction, State
from pythonium.engine.types import VarInt
from pythonium.registries.base import Registry

type ProtocolInfo = tuple[State, Direction, VarInt]


class ProtocolRegistry(Registry[ProtocolInfo]):
    """Protocol registry."""

    __registry_path__ = Path(__file__).parent / "packet_data.json"

    def discover(self) -> Self:
        with self.__registry_path__.open("r", encoding="utf-8") as file:
            data = json.load(file)

        for full_key, (direction, state, packet_id) in data.items():
            self.register(
                full_key,
                (
                    State[state],
                    Direction[direction],
                    packet_id,
                ),
            )

        return self


PROTOCOL_REGISTRY = ProtocolRegistry().discover()
