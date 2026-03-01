from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Int, VarInt


class ChunkDataAndUpdateLight(Packet, kw_only=True):
    """Packet representing ChunkDataAndUpdateLight (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x2C

    chunk_x: Int
    """Int - Chunk coordinate (block coordinate divided by 16, rounded down)"""

    chunk_z: Int
    """Int - Chunk coordinate (block coordinate divided by 16, rounded down)"""

    data: Any  # TODO: Chunk Data
    """Chunk Data"""

    light: Any  # TODO: Light Data
    """Light Data"""
