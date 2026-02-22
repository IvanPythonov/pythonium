from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Slot, VarInt


class SetPlayerInventorySlot(Packet, kw_only=True):
    """Packet representing SetPlayerInventorySlot (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x6A

    slot: VarInt
    """
    VarInt - Index of the slot to be modified in the player inventory.Nota
    container window slot index, to the survival inventory or any other
    window—there is no crafting grid, and the slot order is different.
    """

    slot_data: Slot
    """Slot"""
