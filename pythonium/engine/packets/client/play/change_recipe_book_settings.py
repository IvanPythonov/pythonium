from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, VarInt


class ChangeRecipeBookSettings(Packet, kw_only=True):
    """Packet representing ChangeRecipeBookSettings (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x2D

    book_id: VarInt
    """VarIntEnum - 0: crafting, 1: furnace, 2: blast furnace, 3: smoker."""

    book_open: Boolean
    """Boolean"""

    filter_active: Boolean
    """Boolean"""
