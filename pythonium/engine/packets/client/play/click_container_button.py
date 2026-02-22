from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class ClickContainerButton(Packet, kw_only=True):
    """Packet representing ClickContainerButton (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x10

    window_id: VarInt
    """VarInt - The ID of the window sent byOpen Screen."""

    button_id: VarInt
    """VarInt - Meaning depends on window type; see below."""
