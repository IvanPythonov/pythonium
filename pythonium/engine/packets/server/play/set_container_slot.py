from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Short, Slot, VarInt


class SetContainerSlot(Packet, kw_only=True):
    """Packet representing SetContainerSlot (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x14

    window_id: VarInt
    """
    VarInt - The window that is being updated. 0 for player inventory. The
    client ignores any packets targeting a Window ID other than the current
    one; see below for exceptions.
    """

    state_id: VarInt
    """
    VarInt - A server-managed sequence number used to avoid
    desynchronization; see#Click Container.
    """

    slot: Short
    """Short - The slot that should be updated."""

    slot_data: Slot
    """Slot"""
