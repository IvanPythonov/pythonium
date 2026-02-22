from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Short, VarInt


class SetHeldItem(Packet, kw_only=True):
    """Packet representing SetHeldItem (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x34

    slot: Short
    """Short - The slot which the player has selected (0–8)."""
