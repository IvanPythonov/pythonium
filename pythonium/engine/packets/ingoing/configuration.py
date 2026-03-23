from typing import ClassVar

from pythonium.engine.packets.base import Packet
from pythonium.engine.types import (
    UUID,
    Boolean,
    Byte,
    Int,
    Long,
    RestBuffer,
    String,
    UByte,
    VarInt,
)


class Settings(Packet, kw_only=True):
    """Packet representing Settings."""

    __packet_name__: ClassVar[str] = "configuration:serverbound:settings"

    locale: String  # e.g en_GB
    view_distance: Byte
    chat_mode: VarInt  # 0: enabled, 1: commands only, 2: hidden
    chat_colors: Boolean
    displayed_skin_parts: UByte
    main_hand: VarInt  # 0: left, 1: right
    enable_text_filtering: Boolean
    allow_server_listings: Boolean
    particle_status: VarInt  # 0: all, 1: decreased, 2: minimal


class CookieResponse(Packet, kw_only=True):
    """Packet representing CookieResponse."""

    __packet_name__: ClassVar[str] = (
        "configuration:serverbound:cookie_response"
    )


class CustomPayload(Packet, kw_only=True):
    """Packet representing CustomPayload."""

    __packet_name__: ClassVar[str] = "configuration:serverbound:custom_payload"

    channel: String
    data: RestBuffer


class FinishConfiguration(Packet, kw_only=True):
    """Packet representing FinishConfiguration."""

    __packet_name__: ClassVar[str] = (
        "configuration:serverbound:finish_configuration"
    )


class KeepAlive(Packet, kw_only=True):
    """Packet representing KeepAlive."""

    __packet_name__: ClassVar[str] = "configuration:serverbound:keep_alive"

    keep_alive_id: Long


class Pong(Packet, kw_only=True):
    """Packet representing Pong."""

    __packet_name__: ClassVar[str] = "configuration:serverbound:pong"

    id_: Int


class ResourcePackReceive(Packet, kw_only=True):
    """Packet representing ResourcePackReceive."""

    __packet_name__: ClassVar[str] = (
        "configuration:serverbound:resource_pack_receive"
    )

    uuid: UUID
    result: VarInt


class SelectKnownPacks(Packet, kw_only=True):
    """Packet representing SelectKnownPacks."""

    __packet_name__: ClassVar[str] = (
        "configuration:serverbound:select_known_packs"
    )


class CustomClickAction(Packet, kw_only=True):
    """Packet representing CustomClickAction."""

    __packet_name__: ClassVar[str] = (
        "configuration:serverbound:custom_click_action"
    )
