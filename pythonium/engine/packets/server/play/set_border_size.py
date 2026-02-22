from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Double, VarInt


class SetBorderSize(Packet, kw_only=True):
    """Packet representing SetBorderSize (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x58

    diameter: Double
    """Double - Length of a single side of the world border, in meters."""
