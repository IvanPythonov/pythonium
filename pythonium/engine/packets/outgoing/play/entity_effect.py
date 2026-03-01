from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Byte, VarInt


class EntityEffect(Packet, kw_only=True):
    """Packet representing EntityEffect (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x82

    entity_id: VarInt
    """VarInt"""

    effect_id: VarInt
    """VarInt - Seethis table."""

    amplifier: VarInt
    """VarInt - Vanilla client displays effect level as Amplifier + 1."""

    duration: VarInt
    """VarInt - Duration in ticks. (-1 for infinite)"""

    flags: Byte
    """Byte - Bit field, see below."""
