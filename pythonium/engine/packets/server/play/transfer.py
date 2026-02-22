from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import String, VarInt


class Transfer(Packet, kw_only=True):
    """Packet representing Transfer (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x7F

    host: String
    """String - The hostname or IP of the server."""

    port: VarInt
    """VarInt - The port of the server."""
