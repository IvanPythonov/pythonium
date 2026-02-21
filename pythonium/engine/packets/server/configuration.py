from typing import Annotated, ClassVar

from pythonium.engine.codecs import (
    NBTCodec,
)
from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.custom import StringCodec
from pythonium.engine.codecs.optional import OptionalCodec
from pythonium.engine.enums import Direction, State
from pythonium.engine.packets import Packet
from pythonium.engine.types import (
    NBTCompound,
    Identifier,
    Int,
    Long,
    VarInt,
)

type IdentifierNBT = Annotated[
    list[tuple[str, dict[str, NBTCompound | None]]],
    ArrayCodec((StringCodec(), OptionalCodec(NBTCodec()))),
]


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

    __state__ = State.CONFIGURATION
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x02

    reason: NBTCompound


class RegistryData(Packet, kw_only=True):
    """Packet representing registry data."""

    __state__ = State.CONFIGURATION
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x07

    registry_id: Identifier
    entries: IdentifierNBT


class FinishConfiguration(Packet, kw_only=True):
    """Packet representing finish configuration."""

    __state__ = State.CONFIGURATION
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x03
