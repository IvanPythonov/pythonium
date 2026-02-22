from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import String, VarInt


class ResetScore(Packet, kw_only=True):
    """Packet representing ResetScore (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x4D

    entity_name: String
    """
    String(32767) - The entity whose score this is. For players, this is
    their username; for other entities, it is their UUID.
    """

    objective_name: String | None = None
    """
    Prefixed OptionalString(32767) - The name of the objective the score
    belongs to.
    """
