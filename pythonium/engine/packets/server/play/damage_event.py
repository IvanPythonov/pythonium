from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Double, VarInt


class DamageEvent(Packet, kw_only=True):
    """Packet representing DamageEvent (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x19

    entity_id: VarInt
    """VarInt - The ID of the entity taking damage"""

    source_type_id: VarInt
    """
    VarInt - The type of damage in theminecraft:damage_typeregistry,
    defined by theRegistry Datapacket.
    """

    source_cause_id: VarInt
    """
    VarInt - The ID + 1 of the entity responsible for the damage, if
    present. If not present, the value is 0
    """

    source_direct_id: VarInt
    """
    VarInt - The ID + 1 of the entity that directly dealt the damage, if
    present. If not present, the value is 0. If this field is present:and
    damage was dealt indirectly, such as by the use of a projectile, this
    field will contain the ID of such projectile;and damage was dealt
    directly, such as by manually attacking, this field will contain the
    same value as Source Cause ID.
    """

    source_position: Any  # TODO: X
    """X - Prefixed Optional"""

    y: Double
    """Double"""

    z: Double
    """Double"""
