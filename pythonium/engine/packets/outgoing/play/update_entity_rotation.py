from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Byte, VarInt


class UpdateEntityRotation(Packet, kw_only=True):
    """Packet representing UpdateEntityRotation (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x36

    entity_id: VarInt
    """VarInt"""

    yaw: Byte
    """Angle - New angle, not a delta."""

    pitch: Byte
    """Angle - New angle, not a delta."""

    on_ground: Boolean
    """Boolean"""
