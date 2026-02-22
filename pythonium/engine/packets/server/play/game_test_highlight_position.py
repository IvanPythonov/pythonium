from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Position, VarInt


class GameTestHighlightPosition(Packet, kw_only=True):
    """Packet representing GameTestHighlightPosition (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x27

    absolute_location: Position
    """Position"""

    relative_location: Position
    """Position"""
