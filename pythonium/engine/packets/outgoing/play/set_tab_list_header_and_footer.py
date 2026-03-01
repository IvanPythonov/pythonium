from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import TextComponent, VarInt


class SetTabListHeaderAndFooter(Packet, kw_only=True):
    """Packet representing SetTabListHeaderAndFooter (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x78

    header: TextComponent
    """
    Text Component - To remove the header, send an empty text
    component:{"text":""}.
    """

    footer: TextComponent
    """
    Text Component - To remove the footer, send an empty text
    component:{"text":""}.
    """
