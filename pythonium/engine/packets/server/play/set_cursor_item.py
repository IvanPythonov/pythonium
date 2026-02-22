from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Slot, VarInt


class SetCursorItem(Packet, kw_only=True):
    """Packet representing SetCursorItem (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x5E

    carried_item: Slot
    """Slot"""
