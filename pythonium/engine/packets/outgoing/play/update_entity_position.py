from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Short, VarInt


class UpdateEntityPosition(Packet, kw_only=True):
    """Packet representing UpdateEntityPosition (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x33

    entity_id: VarInt
    """VarInt"""

    delta_x: Short
    """Short - Change in X position ascurrentX * 4096 - prevX * 4096."""

    delta_y: Short
    """Short - Change in Y position ascurrentY * 4096 - prevY * 4096."""

    delta_z: Short
    """Short - Change in Z position ascurrentZ * 4096 - prevZ * 4096."""

    on_ground: Boolean
    """Boolean"""
