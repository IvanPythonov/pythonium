from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Position, String, VarInt


class UpdateSign(Packet, kw_only=True):
    """Packet representing UpdateSign (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x3B

    location: Position
    """Position - Block Coordinates."""

    is_front_text: Boolean
    """
    Boolean - Whether the updated text is in front or on the back of the
    sign
    """

    line_1: String
    """String(384) - First line of text in the sign."""

    line_2: String
    """String(384) - Second line of text in the sign."""

    line_3: String
    """String(384) - Third line of text in the sign."""

    line_4: String
    """String(384) - Fourth line of text in the sign."""
