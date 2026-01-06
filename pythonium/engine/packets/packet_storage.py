from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets import Packet


class PacketStorage:
    """Packet storage."""

    _packets: ClassVar[dict[tuple[int, State, Direction], type[Packet]]] = {}

    @classmethod
    def add(cls, packet: type[Packet]) -> None:
        key = (packet.packet_id, packet.__state__, packet.__direction__)
        if key in cls._packets:
            msg = f"Duplicate packet: {key}"
            raise RuntimeError(msg)
        cls._packets[key] = packet

    @classmethod
    def get(
        cls, packet_id: int, state: State, direction: Direction
    ) -> type[Packet]:
        try:
            return cls._packets[(packet_id, state, direction)]
        except KeyError as error:
            msg = f"Unknown packet {packet_id:#x} in {state}/{direction}"
            raise ValueError(msg) from error
