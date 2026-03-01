from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Position, VarInt


class QueryBlockEntityTag(Packet, kw_only=True):
    """Packet representing QueryBlockEntityTag (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x01

    transaction_id: VarInt
    """
    VarInt - An incremental ID so that the client can verify that the
    response matches.
    """

    location: Position
    """Position - The location of the block to check."""
