from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import UByte, VarInt


class EntityAnimation(Packet, kw_only=True):
    """Packet representing EntityAnimation (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x02

    entity_id: VarInt
    """VarInt - Player ID."""

    animation: UByte
    """Unsigned Byte - Animation ID (see below)."""
