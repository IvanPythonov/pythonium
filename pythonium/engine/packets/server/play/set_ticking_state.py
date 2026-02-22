from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Float, VarInt


class SetTickingState(Packet, kw_only=True):
    """Packet representing SetTickingState (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x7D

    tick_rate: Float
    """Float"""

    is_frozen: Boolean
    """Boolean"""
