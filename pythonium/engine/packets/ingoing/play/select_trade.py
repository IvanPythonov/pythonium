from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class SelectTrade(Packet, kw_only=True):
    """Packet representing SelectTrade (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x32

    selected_slot: VarInt
    """
    VarInt - The selected slot in the player's current (trading) inventory.
    """
