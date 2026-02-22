from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class OpenBook(Packet, kw_only=True):
    """Packet representing OpenBook (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x38

    hand: VarInt
    """VarIntEnum - 0: Main hand, 1: Off hand ."""
