from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class AcknowledgeBlockChange(Packet, kw_only=True):
    """Packet representing AcknowledgeBlockChange (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x04

    sequence_id: VarInt
    """
    VarInt - Represents the sequence to acknowledge; this is used for
    properly syncing block changes to the client after interactions.
    """
