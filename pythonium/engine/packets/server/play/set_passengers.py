from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class SetPassengers(Packet, kw_only=True):
    """Packet representing SetPassengers (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x69

    entity_id: VarInt
    """VarInt - Vehicle's EID."""

    passengers: Any  # TODO: Prefixed ArrayofVarInt
    """Prefixed ArrayofVarInt - EIDs of entity's passengers."""
