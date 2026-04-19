from typing import Any, Self

from pythonium.engine.ticker.tickable import Tickable
from pythonium.registries.block_registry import BLOCK_REGISTRY
from pythonium.worldgen.terrain.base import Chunk, IWorldGenerator
from pythonium.worldgen.terrain.flat import FlatWorldGenerator


class World:
    """Class representing game world."""

    def __init__(self) -> None:
        self.chunks: dict[tuple[int, int], Chunk] = {}

        self.entities: set[Tickable] = set()
        self.blocks_to_tick: list[Tickable] = []

        self.world_generator: IWorldGenerator = FlatWorldGenerator()

    def add_entity(self, entity: Tickable) -> Self:
        self.entities.add(entity)
        return self

    def remove_entity(self, entity: Tickable) -> Self:
        self.entities.discard(entity)
        return self

    def get_id(self, block_name: str, **kwargs: Any) -> int:  # noqa: ANN401
        return BLOCK_REGISTRY.get_id(block_name, **kwargs)

    async def remove_block(self, x: int, y: int, z: int) -> None:
        chunk = await self.get_chunk(x >> 4, z >> 4)
        chunk.set_block(x, y, z, 0)

    async def set_block(self, x: int, y: int, z: int, block_id: int) -> None:
        chunk = await self.get_chunk(x >> 4, z >> 4)
        chunk.set_block(x, y, z, block_id)

    async def get_chunk(self, x: int, z: int) -> Chunk:
        if (x, z) not in self.chunks:
            self.chunks[(x, z)] = self.world_generator.generate_chunk(x, z)
        return self.chunks[(x, z)]

    def tick(self, current_tick: int) -> None:
        for entity in tuple(self.entities):
            entity.tick(current_tick)
