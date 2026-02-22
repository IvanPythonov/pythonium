from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Double, VarInt


class SetBorderCenter(Packet, kw_only=True):
    """Packet representing SetBorderCenter (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x56

    x: Double
    """Double"""

    z: Double
    """Double"""
