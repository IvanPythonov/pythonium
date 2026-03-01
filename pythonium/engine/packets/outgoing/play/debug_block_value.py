from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Position, VarInt


class DebugBlockValue(Packet, kw_only=True):
    """Packet representing DebugBlockValue (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x1A

    location: Position
    """Position"""

    update: Any  # TODO: Debug Subscription Update
    """Debug Subscription Update"""
