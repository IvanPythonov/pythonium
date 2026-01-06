from pythonium.engine.enums import Direction, State
from pythonium.engine.packets import Packet
from pythonium.engine.types import String, UnsignedShortCodec, VarInt


class Handshake(Packet, kw_only=True):
    """Packet representing handshake."""

    __state__ = State.HANDSHAKING
    __direction__ = Direction.SERVERBOUND

    packet_id: VarInt = 0x00
    server_address: String
    server_port: UnsignedShortCodec
    intent: VarInt
