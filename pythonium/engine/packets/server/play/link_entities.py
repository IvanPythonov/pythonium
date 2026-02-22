from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Int, VarInt


class LinkEntities(Packet, kw_only=True):
    """Packet representing LinkEntities (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x62

    attached_entity_id: Int
    """Int - Attached entity's EID."""

    holding_entity_id: Int
    """Int - ID of the entity holding the lead. Set to -1 to detach."""
