from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Position, VarInt


class OpenSignEditor(Packet, kw_only=True):
    """Packet representing OpenSignEditor (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x3A

    location: Position
    """Position"""

    is_front_text: Boolean
    """
    Boolean - Whether the opened editor is for the front or on the back of
    the sign
    """
