from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets import Packet
from pythonium.engine.types import (
    Boolean,
    Byte,
    Int,
    Long,
    String,
    UByte,
    VarInt,
)


class ClientInformation(Packet, kw_only=True):
    """Packet representing client information."""

    __state__ = State.CONFIGURATION
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x00

    locale: String  # e.g en_GB
    view_distance: Byte
    chat_mode: VarInt  # 0: enabled, 1: commands only, 2: hidden
    chat_colors: Boolean
    displayed_skin_parts: UByte
    main_hand: VarInt  # 0: left, 1: right
    enable_text_filtering: Boolean
    allow_server_listings: Boolean
    particle_status: VarInt  # 0: all, 1: decreased, 2: minimal


class PongConfiguration(Packet, kw_only=True):
    """Packet representing pong configuration."""

    __state__ = State.CONFIGURATION
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x05

    id_: Int


class KeepAliveConfigurationRequest(Packet, kw_only=True):
    """Packet representing keep alive configuration."""

    __state__ = State.CONFIGURATION
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x04

    keep_alive_id: Long


class ConfigurationCustomPayload(Packet, kw_only=True):
    """Packet representing configuration custom payload."""

    __state__ = State.CONFIGURATION
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x02

    brand: String
    data: String


class AcknowledgeFinishConfiguration(Packet, kw_only=True):
    """Packet representing finish configuration."""

    __state__ = State.CONFIGURATION
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x03
