from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, VarInt


class PickItemFromEntity(Packet, kw_only=True):
    """Packet representing PickItemFromEntity (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x24

    entity_id: VarInt
    """VarInt - The ID of the entity to pick."""

    include_data: Boolean
    """Boolean - Unused by the vanilla server."""
