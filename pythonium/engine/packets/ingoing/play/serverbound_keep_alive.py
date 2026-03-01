from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Long, VarInt


class ServerboundKeepAlive(Packet, kw_only=True):
    """Packet representing ServerboundKeepAlive (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x1B

    keep_alive_id: Long
    """Long"""
