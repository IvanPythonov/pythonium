from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import TextComponent, VarInt


class SetActionBarText(Packet, kw_only=True):
    """Packet representing SetActionBarText (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x55

    action_bar_text: TextComponent
    """Text Component"""
