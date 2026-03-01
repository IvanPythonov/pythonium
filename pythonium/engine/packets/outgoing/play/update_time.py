from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Long, VarInt


class UpdateTime(Packet, kw_only=True):
    """Packet representing UpdateTime (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x6F

    world_age: Long
    """Long - In ticks; not changed by server commands."""

    time_of_day: Long
    """Long - The world (or region) time, in ticks."""

    time_of_day_increasing: Boolean
    """
    Boolean - If true, the client should automatically advance the time of
    day according to its ticking rate.
    """
