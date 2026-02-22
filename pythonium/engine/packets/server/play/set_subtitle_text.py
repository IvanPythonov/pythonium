from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import TextComponent, VarInt


class SetSubtitleText(Packet, kw_only=True):
    """Packet representing SetSubtitleText (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x6E

    subtitle_text: TextComponent
    """Text Component"""
