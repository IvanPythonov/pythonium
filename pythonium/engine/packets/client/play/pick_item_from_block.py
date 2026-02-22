from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Position, VarInt


class PickItemFromBlock(Packet, kw_only=True):
    """Packet representing PickItemFromBlock (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x23

    location: Position
    """Position - The location of the block."""

    include_data: Boolean
    """
    Boolean - Used to tell the server to include block data in the new
    stack, works only if in creative mode.
    """
