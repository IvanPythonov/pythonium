from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, UByte, VarInt


class ChangeDifficulty(Packet, kw_only=True):
    """Packet representing ChangeDifficulty (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x0A

    difficulty: UByte
    """Unsigned ByteEnum - 0: peaceful, 1: easy, 2: normal, 3: hard."""

    difficulty_locked: Boolean
    """Boolean"""
