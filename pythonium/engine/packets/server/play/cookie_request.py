from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Identifier, VarInt


class CookieRequest(Packet, kw_only=True):
    """Packet representing CookieRequest (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x15

    key: Identifier
    """Identifier - The identifier of the cookie."""
