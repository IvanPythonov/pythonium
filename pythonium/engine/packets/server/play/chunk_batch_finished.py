from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class ChunkBatchFinished(Packet, kw_only=True):
    """Packet representing ChunkBatchFinished (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x0B

    batch_size: VarInt
    """VarInt - Number of chunks."""
