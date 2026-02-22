from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class QueryEntityTag(Packet, kw_only=True):
    """Packet representing QueryEntityTag (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x18

    transaction_id: VarInt
    """
    VarInt - An incremental ID so that the client can verify that the
    response matches.
    """

    entity_id: VarInt
    """VarInt - The ID of the entity to query."""
