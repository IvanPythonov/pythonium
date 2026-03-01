from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class SetCenterChunk(Packet, kw_only=True):
    """Packet representing SetCenterChunk (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x5C

    chunk_x: VarInt
    """VarInt - Chunk X coordinate of the loading area center."""

    chunk_z: VarInt
    """VarInt - Chunk Z coordinate of the loading area center."""
