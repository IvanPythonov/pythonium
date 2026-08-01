from typing import TYPE_CHECKING

from pythonium.engine.packets.base import Packet
from pythonium.engine.packets.outgoing import EntityDestroy
from pythonium.engine.packets.outgoing.play import EntityMetadata, SpawnEntity

if TYPE_CHECKING:
    from pythonium.engine.entity.base import Entity
    from pythonium.engine.server.network import Network
    from pythonium.engine.world import World


def encode_velocity(velocity: float) -> int:
    velocity = max(-3.9, min(3.9, velocity))
    return int(velocity * 8000)


class EntityTracker:
    """Entity tracker."""

    def __init__(self, network: Network, world: World) -> None:
        self.network = network
        self.world = world

    async def spawn_entity(
        self,
        entity: Entity,
    ) -> None:
        spawn_packet = SpawnEntity(
            entity_id=entity.entity_id,
            object_uuid=str(entity.object_uuid),
            type_=entity.entity_type,
            x=entity.x,
            y=entity.y,
            z=entity.z,
            pitch=0,
            yaw=0,
            head_pitch=0,
            velocity_x=encode_velocity(entity.velocity_x),
            velocity_y=encode_velocity(entity.velocity_y),
            velocity_z=encode_velocity(entity.velocity_z),
            object_data=0,
        )

        metadata_packet = EntityMetadata(
            entity_id=entity.entity_id,
            metadata=entity.metadata.copy(),
        )

        entity.popdirty_metadata()

        await self.network.broadcast_many(spawn_packet, metadata_packet)

    async def tick(self) -> None:
        packets: list[Packet] = []
        entities_to_remove_from_memory: list[int] = []

        for entity in list(self.server.world.entities.values()):
            if entity.removed:
                packets.append(EntityDestroy(entity_ids=[entity.entity_id]))
                entities_to_remove_from_memory.append(entity.entity_id)
                continue

            dirty = entity.popdirty_metadata()
            if dirty:
                packets.append(
                    EntityMetadata(entity_id=entity.entity_id, metadata=dirty)
                )

        for eid in entities_to_remove_from_memory:
            self.world.remove_entity(eid)

        if packets:
            await self.network.broadcast_many(*packets)
