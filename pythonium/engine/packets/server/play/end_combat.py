from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class EndCombat(Packet, kw_only=True):
    """Packet representing EndCombat (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x40

    duration: VarInt
    """VarInt - Length of the combat in ticks."""
