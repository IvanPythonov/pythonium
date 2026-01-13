from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets import Packet
from pythonium.engine.types import Long, VarInt


class GetStatus(Packet, kw_only=True):
    """Packet representing status."""

    __state__ = State.STATUS
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x00


class Ping(Packet, kw_only=True):
    """Packet representing ping."""

    __state__ = State.STATUS
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x01

    time: Long
