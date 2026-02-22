from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Int, VarInt


class UnloadChunk(Packet, kw_only=True):
    """Packet representing UnloadChunk (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x25

    chunk_z: Int
    """Int - Block coordinate divided by 16, rounded down."""

    chunk_x: Int
    """Int - Block coordinate divided by 16, rounded down."""
