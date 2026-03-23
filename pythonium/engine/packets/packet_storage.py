from typing import TYPE_CHECKING, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.exceptions import PacketNotFoundError

if TYPE_CHECKING:
    from pythonium.engine.packets.base import Packet


class PacketStorage:
    """O(1) packet storage."""

    _packets: ClassVar[dict[tuple[int, State, Direction], type["Packet"]]] = {}

    @classmethod
    def add(cls, packet: type["Packet"]) -> None:
        key = (packet.packet_id, packet.state, packet.direction)
        if key in cls._packets:
            return
        cls._packets[key] = packet

    @classmethod
    def get(
        cls, packet_id: int, state: State, direction: Direction
    ) -> type["Packet"]:
        try:
            return cls._packets[(packet_id, state, direction)]
        except KeyError as error:
            raise PacketNotFoundError(
                packet_id=f"{packet_id:#04x}",
                state=state.name,
                direction=direction.name,
            ) from error
