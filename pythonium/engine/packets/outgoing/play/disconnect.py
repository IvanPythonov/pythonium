from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import TextComponent, VarInt


class Disconnect(Packet, kw_only=True):
    """Packet representing Disconnect (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x20

    reason: TextComponent
    """
    Text Component - Displayed to the client when the connection
    terminates.
    """
