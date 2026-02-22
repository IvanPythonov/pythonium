from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, VarInt


class ChangeContainerSlotState(Packet, kw_only=True):
    """Packet representing ChangeContainerSlotState (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x13

    slot_id: VarInt
    """VarInt - This is the ID of the slot that was changed."""

    window_id: VarInt
    """VarInt - This is the ID of the window that was changed."""

    state: Boolean
    """
    Boolean - The new state of the slot. True for enabled, false for
    disabled.
    """
