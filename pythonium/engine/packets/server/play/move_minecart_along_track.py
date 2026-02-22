from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Byte, Double, Float, VarInt


class MoveMinecartAlongTrack(Packet, kw_only=True):
    """Packet representing MoveMinecartAlongTrack (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x35

    entity_id: VarInt
    """VarInt"""

    steps: Any  # TODO: X
    """X - Prefixed Array"""

    y: Double
    """Double"""

    z: Double
    """Double"""

    velocity_x: Double
    """Double"""

    velocity_y: Double
    """Double"""

    velocity_z: Double
    """Double"""

    yaw: Byte
    """Angle"""

    pitch: Byte
    """Angle"""

    weight: Float
    """Float"""
