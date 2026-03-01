from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Position, UByte, VarInt


class SetBlockDestroyStage(Packet, kw_only=True):
    """Packet representing SetBlockDestroyStage (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x05

    entity_id: VarInt
    """VarInt - The ID of the entity breaking the block."""

    location: Position
    """Position - Block Position."""

    destroy_stage: UByte
    """Unsigned Byte - 0–9 to set it, any other value to remove it."""
