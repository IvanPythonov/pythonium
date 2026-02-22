from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Int, VarInt


class ChunkBiomes(Packet, kw_only=True):
    """Packet representing ChunkBiomes (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x0D

    chunk_biome_data: Any  # TODO: Chunk Z
    """Chunk Z - Prefixed Array"""

    chunk_x: Int
    """Int - Chunk coordinate (block coordinate divided by 16, rounded down)"""

    data: Any  # TODO: Prefixed ArrayofByte
    """
    Prefixed ArrayofByte - Chunkdata structure, withsectionscontaining only
    theBiomesfield
    """
