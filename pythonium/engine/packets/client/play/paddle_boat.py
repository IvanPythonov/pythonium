from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, VarInt


class PaddleBoat(Packet, kw_only=True):
    """Packet representing PaddleBoat (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x22

    left_paddle_turning: Boolean
    """Boolean"""

    right_paddle_turning: Boolean
    """Boolean"""
