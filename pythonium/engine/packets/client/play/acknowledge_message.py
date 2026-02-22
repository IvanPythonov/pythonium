from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class AcknowledgeMessage(Packet, kw_only=True):
    """Packet representing AcknowledgeMessage (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x05

    message_count: VarInt
    """VarInt"""
