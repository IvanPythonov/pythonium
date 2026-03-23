from typing import ClassVar

from pythonium.engine.packets.base import Packet
from pythonium.engine.types import UUID, RestBuffer, String, VarInt


class LoginStart(Packet, kw_only=True):
    """Packet representing LoginStart."""

    __packet_name__: ClassVar[str] = "login:serverbound:login_start"

    username: String
    player_uuid: UUID


class EncryptionBegin(Packet, kw_only=True):
    """Packet representing EncryptionBegin."""

    __packet_name__: ClassVar[str] = "login:serverbound:encryption_begin"

    shared_secret: bytes
    verify_token: bytes


class LoginPluginResponse(Packet, kw_only=True):
    """Packet representing LoginPluginResponse."""

    __packet_name__: ClassVar[str] = "login:serverbound:login_plugin_response"

    message_id: VarInt
    data: RestBuffer


class LoginAcknowledged(Packet, kw_only=True):
    """Packet representing LoginAcknowledged."""

    __packet_name__: ClassVar[str] = "login:serverbound:login_acknowledged"


class CookieResponse(Packet, kw_only=True):
    """Packet representing CookieResponse."""

    __packet_name__: ClassVar[str] = "login:serverbound:cookie_response"
