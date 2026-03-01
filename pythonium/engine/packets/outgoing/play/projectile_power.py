from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Double, VarInt


class ProjectilePower(Packet, kw_only=True):
    """Packet representing ProjectilePower (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x85

    entity_id: VarInt
    """VarInt"""

    power: Double
    """Double"""
