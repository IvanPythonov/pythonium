from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import String, VarInt


class RenameItem(Packet, kw_only=True):
    """Packet representing RenameItem (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x2F

    item_name: String
    """String(32767) - The new name of the item."""
