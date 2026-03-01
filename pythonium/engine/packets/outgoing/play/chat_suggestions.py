from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class ChatSuggestions(Packet, kw_only=True):
    """Packet representing ChatSuggestions (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x17

    action: VarInt
    """VarIntEnum - 0: Add, 1: Remove, 2: Set"""

    entries: Any  # TODO: Prefixed ArrayofString(32767)
    """Prefixed ArrayofString(32767)"""
