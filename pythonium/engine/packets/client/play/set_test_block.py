from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Position, String, VarInt


class SetTestBlock(Packet, kw_only=True):
    """Packet representing SetTestBlock (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x3A

    position: Position
    """Position"""

    mode: VarInt
    """VarIntEnum - 0: start, 1: log, 2: fail, 3: accept"""

    message: String
    """String"""
