from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import TextComponent, VarInt


class CommandSuggestionsResponse(Packet, kw_only=True):
    """Packet representing CommandSuggestionsResponse (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x0F

    id_: VarInt
    """VarInt - Transaction ID."""

    start: VarInt
    """VarInt - Start of the text to replace."""

    length: VarInt
    """VarInt - Length of the text to replace."""

    matches: Any  # TODO: Match
    """Match - Prefixed Array"""

    tooltip: TextComponent | None = None
    """Prefixed OptionalText Component - Tooltip to display."""
