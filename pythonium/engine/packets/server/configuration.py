from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets import Packet
from pythonium.engine.types import (
    Int,
    Long,
    VarInt,
)


class PingConfiguration(Packet, kw_only=True):
    """Packet representing pong configuration."""

    __state__ = State.CONFIGURATION
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x05

    id_: Int


class KeepAliveConfigurationResponse(Packet, kw_only=True):
    """Packet representing keep alive configuration."""

    __state__ = State.CONFIGURATION
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x04

    keep_alive_id: Long


class Disconnect(Packet, kw_only=True):
    """Packet representing disconnect."""

    __schema_as_json__ = True

    __state__ = State.CONFIGURATION
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x02

    text: str


class FinishConfiguration(Packet, kw_only=True):
    """Packet representing finish configuration."""

    __state__ = State.CONFIGURATION
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x03
