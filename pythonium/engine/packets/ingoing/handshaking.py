from typing import ClassVar

from pythonium.engine.packets.base import Packet
from pythonium.engine.types import (
    String,
    UByte,
    UShort,
    VarInt,
)


class SetProtocol(Packet, kw_only=True):
    """Packet representing SetProtocol."""

    __packet_name__: ClassVar[str] = "handshaking:serverbound:set_protocol"

    protocol_version: VarInt
    server_host: String
    server_port: UShort
    next_state: VarInt


class LegacyServerListPing(Packet, kw_only=True):
    """Packet representing LegacyServerListPing."""

    __packet_name__: ClassVar[str] = (
        "handshaking:serverbound:legacy_server_list_ping"
    )

    payload: UByte
