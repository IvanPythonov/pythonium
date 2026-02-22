from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Double, Float, VarInt


class MoveVehicle(Packet, kw_only=True):
    """Packet representing MoveVehicle (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x21

    x: Double
    """Double - Absolute position (X coordinate)."""

    y: Double
    """Double - Absolute position (Y coordinate)."""

    z: Double
    """Double - Absolute position (Z coordinate)."""

    yaw: Float
    """Float - Absolute rotation on the vertical axis, in degrees."""

    pitch: Float
    """Float - Absolute rotation on the horizontal axis, in degrees."""

    on_ground: Boolean
    """Boolean - (This value does not seem to exist)"""
