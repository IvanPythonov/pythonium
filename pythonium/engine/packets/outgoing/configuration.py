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
    Identifier,
    Int,
    Long,
    NBTCompound,
    TextComponent,
    VarInt,
)

type IdentifierNBT = Annotated[
    list[tuple[str, dict[str, NBTCompound | None]]],
    ArrayCodec((StringCodec(), OptionalCodec(NBTCodec()))),
]


class PingConfiguration(Packet, kw_only=True):
    """Packet representing pong configuration."""

    __state__: ClassVar[State] = State.CONFIGURATION
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x05

    id_: Int


class KeepAliveConfigurationResponse(Packet, kw_only=True):
    """Packet representing keep alive configuration."""

    __state__: ClassVar[State] = State.CONFIGURATION
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x04

    keep_alive_id: Long


class ConfigurationDisconnect(Packet, kw_only=True):
    """Packet representing disconnect."""

    __state__: ClassVar[State] = State.CONFIGURATION
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x02

    reason: TextComponent


class RegistryData(Packet, kw_only=True):
    """Packet representing registry data."""

    __state__: ClassVar[State] = State.CONFIGURATION
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x07

    registry_id: Identifier
    entries: IdentifierNBT


class FinishConfiguration(Packet, kw_only=True):
    """Packet representing finish configuration."""

    __state__: ClassVar[State] = State.CONFIGURATION
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x03
