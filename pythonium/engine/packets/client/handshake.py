from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets import Packet
from pythonium.engine.types import String, UShort, VarInt


class Handshake(Packet, kw_only=True):
    """Packet representing handshake."""

    __state__ = State.HANDSHAKING
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x00

    protocol_version: VarInt

    server_address: String
    server_port: UShort

    next_state: VarInt
