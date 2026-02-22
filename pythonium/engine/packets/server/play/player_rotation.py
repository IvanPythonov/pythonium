from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Float, VarInt


class PlayerRotation(Packet, kw_only=True):
    """Packet representing PlayerRotation (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x47

    yaw: Float
    """Float - Rotation on the X axis, in degrees."""

    relative_yaw: Boolean
    """Boolean"""

    pitch: Float
    """Float - Rotation on the Y axis, in degrees."""

    relative_pitch: Boolean
    """Boolean"""
