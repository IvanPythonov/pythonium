from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Float, VarInt


class ChunkBatchReceived(Packet, kw_only=True):
    """Packet representing ChunkBatchReceived (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x0A

    chunks_per_tick: Float
    """Float - Desired chunks per tick."""
