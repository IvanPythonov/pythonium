from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import String, VarInt


class ServerLinks(Packet, kw_only=True):
    """Packet representing ServerLinks (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x87

    links: Any  # TODO: Is built-in
    """Is built-in - Prefixed Array"""

    label: VarInt
    """VarIntEnum/Text Component - See below."""

    url: String
    """String - Valid URL."""
