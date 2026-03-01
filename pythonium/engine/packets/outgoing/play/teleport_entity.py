from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Double, Float, VarInt


class TeleportEntity(Packet, kw_only=True):
    """Packet representing TeleportEntity (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x23

    entity_id: VarInt
    """VarInt"""

    x: Double
    """Double"""

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

    yaw: Float
    """Float - Rotation on the X axis, in degrees."""

    pitch: Float
    """Float - Rotation on the Y axis, in degrees."""

    on_ground: Boolean
    """Boolean"""
