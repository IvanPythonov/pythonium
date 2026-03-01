from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, TextComponent, VarInt


class SystemChatMessage(Packet, kw_only=True):
    """Packet representing SystemChatMessage (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x77

    content: TextComponent
    """Text Component - Limited to 262144 bytes."""

    overlay: Boolean
    """
    Boolean - Whether the message is an actionbar or chat message. See
    also#Set Action Bar Text.
    """
