import struct
from array import array
from collections.abc import Collection
from typing import Protocol

from pythonium.engine.codecs import VarIntCodec
from pythonium.engine.codecs.chunk import LightDataStruct
from pythonium.engine.constants import MAX_WORLD_HEIGHT, MIN_WORLD_HEIGHT
from pythonium.engine.exceptions import ChunkSectionOutOfBoundsError

_varint = VarIntCodec()

MIN_BPE = 4
MAX_BPE = 8
GLOBAL_BPE = 15
BITS_PER_LONG = 64

EMPTY_SECTION_BYTES = b"\x00\x00\x00\x00\x00\x01"
FULL_BRIGHT_SECTION = b"\xff" * 2048


class ChunkSection:
    """Represents a 16x16x16 area of a chunk with its own palette."""

    __slots__ = ("__blocks", "_non_air_count", "_palette_cache")

    def __init__(self) -> None:
        self._palette_cache: dict[int, int] = {0: 4096}
        self._non_air_count = 0
        self.__blocks = array("H", [0] * 4096)

    def get_block(self, x: int, y: int, z: int) -> int:
        return self.__blocks[(y << 8) | (z << 4) | x]

    def set_block(self, x: int, y: int, z: int, block_data: int) -> None:
        index = (y << 8) | (z << 4) | x
        old_id = self.get_block(x, y, z)
        if old_id == block_data:
            return

        self._palette_cache[old_id] -= 1

        if self._palette_cache[old_id] == 0:
            del self._palette_cache[old_id]

        self._palette_cache[block_data] = (
            self._palette_cache.get(block_data, 0) + 1
        )

        if old_id == 0 and block_data != 0:
            self._non_air_count += 1

        if old_id != 0 and block_data == 0:
            self._non_air_count -= 1

        self.__blocks[index] = block_data

    def get_palette(self) -> list[int]:
        return list(self._palette_cache.keys())

    def calculate_bpe(self) -> int:
        palette_size = len(self.get_palette())
        if palette_size <= 1:
            return 0
        bits = (palette_size - 1).bit_length()
        if bits <= MIN_BPE:
            return MIN_BPE
        return bits if bits <= MAX_BPE else GLOBAL_BPE

    def get_non_air_count(self) -> int:
        return self._non_air_count

    def serialize_data_array(
        self, bpe: int, entries: Collection[int]
    ) -> bytes:
        if bpe == 0:
            return b""

        current_bit_offset = 0
        current_long_idx = 0

        entries_per_long = BITS_PER_LONG // bpe
        long_count = (len(entries) + entries_per_long - 1) // entries_per_long
        longs = array("Q", [0] * long_count)
        mask = (1 << bpe) - 1

        for val in entries:
            longs[current_long_idx] |= (val & mask) << current_bit_offset
            current_bit_offset += bpe
            if current_bit_offset + bpe > BITS_PER_LONG:
                current_bit_offset = 0
                current_long_idx += 1

        longs.byteswap()
        return longs.tobytes()

    def encode_block_container(self) -> bytes:
        palette = self._palette_cache.keys()
        bpe = (
            0 if len(palette) <= 1 else max(4, (len(palette) - 1).bit_length())
        )
        if bpe > MAX_BPE:
            bpe = 15

        res = bytearray([bpe])
        if bpe == 0:
            res.extend(_varint.serialize(field=next(iter(palette))))
        elif bpe <= MAX_BPE:
            res.extend(_varint.serialize(field=len(palette)))
            for p_id in palette:
                res.extend(_varint.serialize(field=p_id))

            p_map = {b_id: i for i, b_id in enumerate(palette)}
            indices = list(map(p_map.__getitem__, self.__blocks))
            data = self.serialize_data_array(bpe, indices)
            res.extend(data)
        else:
            data = self.serialize_data_array(bpe, self.__blocks)
            res.extend(data)

        return bytes(res)

    def encode_biome_container(self) -> bytes:
        return b"\x00" + _varint.serialize(field=1)

    def set_blocks_from_array(self, block_array: array) -> None:
        self.__blocks = array("H", block_array)
        self._palette_cache.clear()
        self._non_air_count = 0

        for block in self.__blocks:
            self._palette_cache[block] = self._palette_cache.get(block, 0) + 1
            if block != 0:
                self._non_air_count += 1


class Chunk:
    """Container for 24 ChunkSections forming a vertical column."""

    __slots__ = ("chunk_data", "chunk_x", "chunk_z")

    def __init__(self, x: int, z: int) -> None:
        self.chunk_x = x
        self.chunk_z = z

        self.chunk_data: list[ChunkSection | None] = [None] * 24

    def get_chunk_data(self) -> bytes:
        buf = bytearray()
        for section in self.chunk_data:
            if section is None:
                buf.extend(EMPTY_SECTION_BYTES)
                continue
            non_air_count = section.get_non_air_count()

            if non_air_count == 0:
                buf.extend(EMPTY_SECTION_BYTES)
            else:
                buf.extend(struct.pack(">h", non_air_count))
                buf.extend(section.encode_block_container())
                buf.extend(section.encode_biome_container())

        return bytes(buf)

    def get_light_data(self) -> LightDataStruct:
        mask = 0x3FFFFFF
        count = mask.bit_count()

        sky_updates = [FULL_BRIGHT_SECTION] * count

        return LightDataStruct(
            sky_y_mask=[mask],
            block_y_mask=[0],
            empty_sky_y_mask=[0],
            empty_block_y_mask=[0],
            sky_updates=sky_updates,
            block_updates=[],
        )

    def get_heightmaps(self) -> dict[str, list[int]]:
        return {
            "MOTION_BLOCKING": [0] * 36,
            "WORLD_SURFACE": [0] * 36,
        }

    def get_block(self, x: int, y: int, z: int) -> int:
        section = self.get_section_for_y(y)
        if section is None:
            return 0
        return section.get_block(x & 0xF, y & 0xF, z & 0xF)

    def set_block(self, x: int, y: int, z: int, block_data: int) -> None:
        section = self.get_section_for_y(y)
        if section is None and block_data == 0:
            return
        if section is None:
            section = self.create_section_for_y(y)

        section.set_block(x & 0xF, y & 0xF, z & 0xF, block_data)

    def get_section_for_y(self, world_y: int) -> ChunkSection | None:
        if not (MIN_WORLD_HEIGHT <= world_y <= MAX_WORLD_HEIGHT):
            raise ChunkSectionOutOfBoundsError(world_y=world_y)
        return self.chunk_data[(world_y >> 4) + 4]

    def create_section_for_y(self, world_y: int) -> ChunkSection:
        if not (MIN_WORLD_HEIGHT <= world_y <= MAX_WORLD_HEIGHT):
            raise ChunkSectionOutOfBoundsError(world_y=world_y)

        idx = (world_y >> 4) + 4
        section = self.chunk_data[idx]
        if section is None:
            section = ChunkSection()
            self.chunk_data[idx] = section

        return section


class IWorldGenerator(Protocol):
    """Interface for terrain generators."""

    def generate_chunk(self, x: int, z: int) -> Chunk: ...
