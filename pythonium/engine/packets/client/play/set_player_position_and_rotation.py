from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Byte, Double, Float, VarInt


class SetPlayerPositionAndRotation(Packet, kw_only=True):
    """Packet representing SetPlayerPositionAndRotation (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x1E

    x: Double
    """Double - Absolute position."""

    feet_y: Double
    """Double - Absolute feet position, normally Head Y - 1.62."""

    z: Double
    """Double - Absolute position."""

    yaw: Float
    """Float - Absolute rotation on the X Axis, in degrees."""

    pitch: Float
    """Float - Absolute rotation on the Y Axis, in degrees."""

    flags: Byte
    """Byte - Bit field: 0x01: on ground, 0x02: pushing against wall."""
