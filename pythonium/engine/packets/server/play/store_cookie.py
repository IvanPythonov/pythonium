from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Identifier, VarInt


class StoreCookie(Packet, kw_only=True):
    """Packet representing StoreCookie (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x76

    key: Identifier
    """Identifier - The identifier of the cookie."""

    payload: Any  # TODO: Prefixed Array(5120) ofByte
    """Prefixed Array(5120) ofByte - The data of the cookie."""
