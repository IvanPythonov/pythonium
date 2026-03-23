from typing import ClassVar

from pythonium.engine.packets.base import Packet
from pythonium.engine.types import (
    UUID,
    Boolean,
    ByteArray,
    RestBuffer,
    String,
    VarInt,
)


class Disconnect(Packet, kw_only=True):
    """Packet representing Disconnect."""

    __packet_name__: ClassVar[str] = "login:clientbound:disconnect"

    reason: String


class EncryptionBegin(Packet, kw_only=True):
    """Packet representing EncryptionBegin."""

    __packet_name__: ClassVar[str] = "login:clientbound:encryption_begin"

    server_id: String
    public_key: ByteArray
    verify_token: ByteArray
    should_authenticate: Boolean


class Success(Packet, kw_only=True):
    """Packet representing Success."""

    __packet_name__: ClassVar[str] = "login:clientbound:success"

    uuid: UUID
    name: String
    is_legacy: Boolean


class Compress(Packet, kw_only=True):
    """Packet representing Compress."""

    __packet_name__: ClassVar[str] = "login:clientbound:compress"

    threshold: VarInt


class LoginPluginRequest(Packet, kw_only=True):
    """Packet representing LoginPluginRequest."""

    __packet_name__: ClassVar[str] = "login:clientbound:login_plugin_request"

    message_id: VarInt
    channel: String
    data: RestBuffer


class CookieRequest(Packet, kw_only=True):
    """Packet representing CookieRequest."""

    __packet_name__: ClassVar[str] = "login:clientbound:cookie_request"
