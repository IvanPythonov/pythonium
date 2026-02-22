from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Double, VarInt


class LookAt(Packet, kw_only=True):
    """Packet representing LookAt (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x45

    feet_eyes: VarInt
    """
    VarIntEnum - Values are feet=0, eyes=1.  If set to eyes, aims using the
    head position; otherwise, aims using the feet position.
    """

    target_x: Double
    """Double - x coordinate of the point to face towards."""

    target_y: Double
    """Double - y coordinate of the point to face towards."""

    target_z: Double
    """Double - z coordinate of the point to face towards."""

    is_entity: Boolean
    """
    Boolean - If true, additional information about an entity is provided.
    """

    entity_id: VarInt | None = None
    """
    OptionalVarInt - Only if is entity is true — the entity to face
    towards.
    """

    entity_feet_eyes: VarInt
    """
    OptionalVarIntEnum - Whether to look at the entity's eyes or feet.
    Same values and meanings as before, just for the entity's head/feet.
    """
