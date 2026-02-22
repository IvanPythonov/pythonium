from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Int, Position, VarInt


class WorldEvent(Packet, kw_only=True):
    """Packet representing WorldEvent (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x2D

    event: Int
    """Int - The event, see below."""

    location: Position
    """Position - The location of the event."""

    data: Int
    """Int - Extra data for certain events, see below."""

    disable_relative_volume: Boolean
    """Boolean - See above."""
