from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class AcknowledgeConfiguration(Packet, kw_only=True):
    """Packet representing AcknowledgeConfiguration (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x0F
