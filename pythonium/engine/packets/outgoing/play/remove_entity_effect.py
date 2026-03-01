from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class RemoveEntityEffect(Packet, kw_only=True):
    """Packet representing RemoveEntityEffect (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x4C

    entity_id: VarInt
    """VarInt"""

    effect_id: VarInt
    """VarInt - Seethis table."""
