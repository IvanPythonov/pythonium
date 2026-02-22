from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class AwardStatistics(Packet, kw_only=True):
    """Packet representing AwardStatistics (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x03

    statistics: Any  # TODO: Category ID
    """Category ID - Prefixed Array"""

    statistic_id: VarInt
    """VarInt - See below."""

    value: VarInt
    """VarInt - The amount to set it to."""
