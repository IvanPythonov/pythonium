from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Position, VarInt


class BlockUpdate(Packet, kw_only=True):
    """Packet representing BlockUpdate (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x08

    location: Position
    """Position - Block Coordinates."""

    block_id: VarInt
    """
    VarInt - The new block state ID for the block as given in theglobal
    block state palette.
    """
