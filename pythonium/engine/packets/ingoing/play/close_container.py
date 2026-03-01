from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class CloseContainer(Packet, kw_only=True):
    """Packet representing CloseContainer (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x12

    window_id: VarInt
    """
    VarInt - This is the ID of the window that was closed. 0 for player
    inventory.
    """
