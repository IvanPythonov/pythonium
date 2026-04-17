from pythonium.registries.block_registry import BLOCK_REGISTRY
from pythonium.worldgen.terrain.base import Chunk, IWorldGenerator


class FlatWorldGenerator(IWorldGenerator):
    """Flat world generator."""

    def generate_chunk(self, x: int, z: int) -> Chunk:
        """Generate chunk data for given coordinates."""
        chunk = Chunk(x, z)

        section = chunk.get_section_for_y(-64)

        for local_x in range(16):
            for local_z in range(16):
                section.set_block(
                    local_x, 0, local_z, BLOCK_REGISTRY.get_id("bedrock")
                )
                section.set_block(
                    local_x, 1, local_z, BLOCK_REGISTRY.get_id("stone")
                )
                section.set_block(
                    local_x, 2, local_z, BLOCK_REGISTRY.get_id("dirt")
                )
                section.set_block(
                    local_x,
                    3,
                    local_z,
                    BLOCK_REGISTRY.get_id("grass_block", snowy=False),
                )

        return chunk
