from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class PickupItem(Packet, kw_only=True):
    """Packet representing PickupItem (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x7A

    collected_entity_id: VarInt
    """VarInt"""

    collector_entity_id: VarInt
    """VarInt"""

    pickup_item_count: VarInt
    """
    VarInt - Seems to be 1 for XP orbs, otherwise the number of items in
    the stack.
    """
