from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Int, VarInt


class DebugChunkValue(Packet, kw_only=True):
    """Packet representing DebugChunkValue (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x1B

    chunk_z: Int
    """Int"""

    chunk_x: Int
    """Int"""

    update: Any  # TODO: Debug Subscription Update
    """Debug Subscription Update"""
