from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets import Packet
from pythonium.engine.types import Long, String, VarInt


class ServerStatus(Packet, kw_only=True):
    """Packet representing status."""

    __state__ = State.STATUS
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x00

    json_response: String


class Pong(Packet, kw_only=True):
    """Packet representing pong."""

    __state__ = State.STATUS
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x01

    time: Long
