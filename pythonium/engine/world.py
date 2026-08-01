from typing import Any, Self

from pythonium.engine.entity.base import Entity
from pythonium.engine.ticker.tickable import Tickable
from pythonium.registries.block_registry import BLOCK_REGISTRY
from pythonium.worldgen.terrain.base import Chunk, IWorldGenerator


class World:
    """Class representing game world."""

    def __init__(self, chunk_generator: IWorldGenerator) -> None:
        self.chunks: dict[tuple[int, int], Chunk] = {}

        self.entities: dict[int, Entity] = {}
        self.blocks_to_tick: list[Tickable] = []

        self.chunk_generator: IWorldGenerator = chunk_generator

        self._next_entity_id = 1

    def add_entity(self, entity: Entity, entity_id: int) -> Self:
        self.entities[entity_id] = entity
        return self

    def remove_entity(self, entity_id: int) -> Self:
        self.entities.pop(entity_id, None)
        return self

    def next_entity_id(self) -> int:
        entity_id = self._next_entity_id
        self._next_entity_id += 1

        return entity_id

    def get_id(self, block_name: str, **kwargs: Any) -> int:  # noqa: ANN401
        return BLOCK_REGISTRY.get_id(block_name, **kwargs)

    async def remove_block(self, x: int, y: int, z: int) -> None:
        chunk = await self.get_chunk(x >> 4, z >> 4)
        chunk.set_block(x, y, z, 0)

    async def set_block(self, x: int, y: int, z: int, block_id: int) -> None:
        chunk = await self.get_chunk(x >> 4, z >> 4)
        chunk.set_block(x, y, z, block_id)

    async def spawn_entity(
        self,
        entity: Entity,
    ) -> Entity:
        entity.entity_id = self.next_entity_id()

        self.entities[entity.entity_id] = entity

        return entity

    async def get_chunk(self, x: int, z: int) -> Chunk:
        if (x, z) not in self.chunks:
            self.chunks[(x, z)] = self.chunk_generator.generate_chunk(x, z)
        return self.chunks[(x, z)]

    def tick(self, current_tick: int) -> None:
        for entity in list(self.entities.values()):
            entity.tick(current_tick)
