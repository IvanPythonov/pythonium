from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class BundleItemSelected(Packet, kw_only=True):
    """Packet representing BundleItemSelected (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x02

    slot_of_bundle: VarInt
    """VarInt"""

    slot_in_bundle: VarInt
    """VarInt"""
