from array import array

from pythonium.registries.block_registry import BLOCK_REGISTRY
from pythonium.worldgen.terrain.base import Chunk, IWorldGenerator


class FlatChunk(Chunk):
    """Flat chunk implementation with lazy block data initialization."""

    __slots__ = ("_cached_payload", "_is_mutated", "_template_array")

    def __init__(
        self, x: int, z: int, cached_payload: bytes, template_array: array
    ) -> None:
        super().__init__(x, z)

        self._cached_payload = cached_payload
        self._template_array = template_array
        self._is_mutated = False

    def get_chunk_data(self) -> bytes:
        if not self._is_mutated:
            return self._cached_payload
        return super().get_chunk_data()

    def set_block(self, x: int, y: int, z: int, block_data: int) -> None:
        if not self._is_mutated:
            self._is_mutated = True

            section = self.create_section_for_y(-64)
            section.set_blocks_from_array(self._template_array)

        super().set_block(x, y, z, block_data)


class FlatWorldGenerator(IWorldGenerator):
    """Flat world generator."""

    def __init__(self) -> None:
        self._ground_template = array("H", [0] * 4096)
        self._generate_ground_template()

        self._baked_payload = self._bake_template_chunk()

    def _generate_ground_template(self) -> None:
        bedrock = BLOCK_REGISTRY.get_id("minecraft:bedrock")
        dirt = BLOCK_REGISTRY.get_id("minecraft:dirt")
        grass = BLOCK_REGISTRY.get_id("minecraft:grass_block", snowy=False)

        for x in range(16):
            for z in range(16):
                self._ground_template[(0 << 8) | (z << 4) | x] = bedrock
                self._ground_template[(1 << 8) | (z << 4) | x] = dirt
                self._ground_template[(2 << 8) | (z << 4) | x] = dirt
                self._ground_template[(3 << 8) | (z << 4) | x] = grass

    def _bake_template_chunk(self) -> bytes:
        temp_chunk = Chunk(0, 0)
        section = temp_chunk.create_section_for_y(-64)
        section.set_blocks_from_array(self._ground_template)
        return temp_chunk.get_chunk_data()

    def generate_chunk(self, x: int, z: int) -> Chunk:
        return FlatChunk(x, z, self._baked_payload, self._ground_template)
