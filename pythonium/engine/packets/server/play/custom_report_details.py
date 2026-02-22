from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import String, VarInt


class CustomReportDetails(Packet, kw_only=True):
    """Packet representing CustomReportDetails (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x86

    details: Any  # TODO: Title
    """Title - Prefixed Array(32)"""

    description: String
    """String(4096)"""
