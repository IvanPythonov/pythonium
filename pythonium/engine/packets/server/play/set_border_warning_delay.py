from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class SetBorderWarningDelay(Packet, kw_only=True):
    """Packet representing SetBorderWarningDelay (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x59

    warning_time: VarInt
    """VarInt - In seconds as set by/worldborder warning time."""
