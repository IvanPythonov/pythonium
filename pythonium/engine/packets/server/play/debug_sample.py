from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class DebugSample(Packet, kw_only=True):
    """Packet representing DebugSample (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x1E

    sample: Any  # TODO: Prefixed ArrayofLong
    """Prefixed ArrayofLong - Array of type-dependent samples."""

    sample_type: VarInt
    """VarIntEnum - See below."""
