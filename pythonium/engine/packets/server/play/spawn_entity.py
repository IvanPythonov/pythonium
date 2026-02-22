from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import UUID, Byte, Double, VarInt


class SpawnEntity(Packet, kw_only=True):
    """Packet representing SpawnEntity (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x01

    entity_id: VarInt
    """
    VarInt - A unique integer ID mostly used in the protocol to identify
    the entity. If an entity with the same ID already exists on the client,
    it is automatically deleted and replaced by the new entity. On the
    vanilla server entity IDs are globally unique across all dimensions and
    never reused while the server is running, but not preserved across
    server restarts.
    """

    entity_uuid: UUID
    """
    UUID - A unique identifier that is mostly used in persistence and
    places where the uniqueness matters more. It is possible to create
    multiple entities with the same UUID on the vanilla client, but a
    warning will be logged, and functionality dependent on UUIDs may ignore
    the entity or otherwise misbehave.
    """

    type_: VarInt
    """
    VarInt - ID in theminecraft:entity_typeregistry (see "type" field
    inJava Edition protocol/Entity metadata#Entities).
    """

    x: Double
    """Double"""

    y: Double
    """Double"""

    z: Double
    """Double"""

    velocity: Any  # TODO: LpVec3
    """LpVec3"""

    pitch: Byte
    """Angle"""

    yaw: Byte
    """Angle"""

    head_yaw: Byte
    """
    Angle - Only used by living entities, where the head of the entity may
    differ from the general body rotation.
    """

    data: VarInt
    """
    VarInt - Meaning dependent on the value of the Type field, seeJava
    Edition protocol/Object datafor details.
    """
