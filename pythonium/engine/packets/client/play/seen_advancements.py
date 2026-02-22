from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Identifier, VarInt


class SeenAdvancements(Packet, kw_only=True):
    """Packet representing SeenAdvancements (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x31

    action: VarInt
    """VarIntEnum - 0: Opened tab, 1: Closed screen."""

    tab_id: Identifier | None = None
    """OptionalIdentifier - Only present if action is Opened tab."""
