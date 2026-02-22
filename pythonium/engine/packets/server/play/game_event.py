from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Float, UByte, VarInt


class GameEvent(Packet, kw_only=True):
    """Packet representing GameEvent (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x26

    event: UByte
    """Unsigned Byte - See below."""

    value: Float
    """Float - Depends on Event."""
