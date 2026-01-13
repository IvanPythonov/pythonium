from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets import Packet
from pythonium.engine.types import Long, String, VarInt


class Status(Packet, kw_only=True):
    """Packet representing status."""

    __state__ = State.STATUS
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x00


class ServerStatus(Packet, kw_only=True):
    """Packet representing status."""

    __state__ = State.STATUS
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x00

    json_response: String


class Ping(Packet, kw_only=True):
    """Packet representing ping."""

    __state__ = State.STATUS
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x01

    time: Long


class Pong(Packet, kw_only=True):
    """Packet representing pong."""

    __state__ = State.STATUS
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x01

    time: Long
