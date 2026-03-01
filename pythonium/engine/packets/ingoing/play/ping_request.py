from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Long, VarInt


class PingRequest(Packet, kw_only=True):
    """Packet representing PingRequest (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x25

    payload: Long
    """
    Long - May be any number. vanilla clients use a system-dependent time
    value, which is counted in milliseconds.
    """
