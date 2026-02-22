from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Int, VarInt


class OpenHorseScreen(Packet, kw_only=True):
    """Packet representing OpenHorseScreen (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x28

    window_id: VarInt
    """VarInt - Same as the field ofOpen Screen."""

    inventory_columns_count: VarInt
    """
    VarInt - How many columns of horse inventory slots exist in the GUI, 3
    slots per column.
    """

    entity_id: Int
    """
    Int - The "owner" entity of the GUI. The client should close the GUI if
    the owner entity dies or is cleared.
    """
