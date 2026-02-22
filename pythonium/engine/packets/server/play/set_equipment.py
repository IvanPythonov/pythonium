from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Slot, VarInt


class SetEquipment(Packet, kw_only=True):
    """Packet representing SetEquipment (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x64

    entity_id: VarInt
    """VarInt - Entity's ID."""

    equipment: Slot
    """Slot - Array"""

    item: Slot
    """Slot"""
