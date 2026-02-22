from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Identifier, VarInt


class SelectAdvancementsTab(Packet, kw_only=True):
    """Packet representing SelectAdvancementsTab (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x53

    identifier: Identifier | None = None
    """Prefixed OptionalIdentifier - See below."""
