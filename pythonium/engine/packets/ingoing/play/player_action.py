from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Byte, Position, VarInt


class PlayerAction(Packet, kw_only=True):
    """Packet representing PlayerAction (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x28

    status: VarInt
    """
    VarIntEnum - The action the player is taking against the block (see
    below).
    """

    location: Position
    """Position - Block position."""

    face: Byte
    """ByteEnum - The face being hit (see below)."""

    sequence: VarInt
    """VarInt - Block change sequence number (see#Acknowledge Block Change)."""
