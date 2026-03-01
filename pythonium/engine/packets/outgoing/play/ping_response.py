from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Long, VarInt


class PingResponse(Packet, kw_only=True):
    """Packet representing PingResponse (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x3C

    payload: Long
    """Long - Should be the same as sent by the client."""
