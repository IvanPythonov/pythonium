from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import TextComponent, VarInt


class ServerData(Packet, kw_only=True):
    """Packet representing ServerData (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x54

    motd: TextComponent
    """Text Component"""

    icon: Any  # TODO: Prefixed ArrayofByte| None = None
    """Prefixed OptionalPrefixed ArrayofByte - Icon bytes in the PNG format."""
