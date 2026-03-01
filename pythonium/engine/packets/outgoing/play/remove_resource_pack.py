from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import UUID, VarInt


class RemoveResourcePack(Packet, kw_only=True):
    """Packet representing RemoveResourcePack (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x4E

    uuid: UUID | None = None
    """OptionalUUID - The UUID of the resource pack to be removed."""
