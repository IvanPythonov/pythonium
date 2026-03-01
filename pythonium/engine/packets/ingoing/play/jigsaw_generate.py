from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Position, VarInt


class JigsawGenerate(Packet, kw_only=True):
    """Packet representing JigsawGenerate (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x1A

    location: Position
    """Position - Block entity location."""

    levels: VarInt
    """VarInt - Value of the levels slider/max depth to generate."""

    keep_jigsaws: Boolean
    """Boolean"""
