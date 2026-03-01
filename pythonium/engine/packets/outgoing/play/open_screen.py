from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import TextComponent, VarInt


class OpenScreen(Packet, kw_only=True):
    """Packet representing OpenScreen (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x39

    window_id: VarInt
    """
    VarInt - An identifier for the window to be displayed. The vanilla
    server implementation is a counter, starting at 1. There can only be
    one window at a time; this is only used to ignore outdated packets
    targeting already-closed windows. Note also that the Window ID field in
    most other packets is only a single byte, and indeed, the vanilla
    server wraps around after 100.
    """

    window_type: VarInt
    """
    VarInt - The window type to use for display. Contained in
    theminecraft:menuregistry; seeJava Edition protocol/Inventoryfor the
    different values.
    """

    window_title: TextComponent
    """Text Component - The title of the window."""
