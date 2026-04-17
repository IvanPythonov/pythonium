import struct
from array import array
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


class ChunkSection:
    """Represents a 16x16x16 area of a chunk with its own palette."""

    __slots__ = ("__blocks",)

    def __init__(self) -> None:
        self.__blocks = array("H", [0] * 4096)

    def get_block(self, x: int, y: int, z: int) -> int:
        return self.__blocks[(y << 8) | (z << 4) | x]

    def set_block(self, x: int, y: int, z: int, block_data: int) -> None:
        self.__blocks[(y << 8) | (z << 4) | x] = block_data

    def get_palette(self) -> list[int]:
        return list(dict.fromkeys(self.__blocks))

    def calculate_bpe(self) -> int:
        palette_size = len(self.get_palette())
        if palette_size <= 1:
            return 0
        bits = (palette_size - 1).bit_length()
        if bits <= MIN_BPE:
            return MIN_BPE
        return bits if bits <= MAX_BPE else GLOBAL_BPE

    def get_non_air_count(self) -> int:
        return 4096 - self.__blocks.count(0)

    def serialize_data_array(self, bpe: int, entries: list[int]) -> bytes:
        if bpe == 0:
            return b""

        entries_per_long = BITS_PER_LONG // bpe
        long_count = (len(entries) + entries_per_long - 1) // entries_per_long
        longs = array("Q", [0] * long_count)
        mask = (1 << bpe) - 1

        for i, val in enumerate(entries):
            long_idx = i // entries_per_long
            bit_offset = (i % entries_per_long) * bpe
            longs[long_idx] |= (val & mask) << bit_offset

        return b"".join(struct.pack(">Q", long) for long in longs)

    def serialize_bit_storage(self, bpe: int, entries: list[int]) -> bytes:
        if bpe == 0:
            return b""

        entries_per_long = 64 // bpe
        long_count = (len(entries) + entries_per_long - 1) // entries_per_long
        longs = array("Q", [0] * long_count)
        mask = (1 << bpe) - 1

        for i, val in enumerate(entries):
            l_idx = i // entries_per_long
            bit_offset = (i % entries_per_long) * bpe
            longs[l_idx] |= (val & mask) << bit_offset

        return b"".join(struct.pack(">Q", long) for long in longs)

    def encode_block_container(self) -> bytes:
        palette = list(dict.fromkeys(self.__blocks))
        bpe = (
            0 if len(palette) <= 1 else max(4, (len(palette) - 1).bit_length())
        )
        if bpe > MAX_BPE:
            bpe = 15

        res = bytearray([bpe])
        if bpe == 0:
            res.extend(_varint.serialize(field=palette[0]))
        elif bpe <= MAX_BPE:
            res.extend(_varint.serialize(field=len(palette)))
            for p_id in palette:
                res.extend(_varint.serialize(field=p_id))

            p_map = {b_id: i for i, b_id in enumerate(palette)}
            indices = [p_map[b] for b in self.__blocks]
            data = self.serialize_bit_storage(bpe, indices)
            res.extend(data)
        else:
            data = self.serialize_bit_storage(bpe, list(self.__blocks))
            res.extend(data)

        return bytes(res)

    def encode_biome_container(self) -> bytes:
        return b"\x00" + _varint.serialize(field=1)


class Chunk:
    """Container for 24 ChunkSections forming a vertical column."""

    __slots__ = ("chunk_data", "chunk_x", "chunk_z")

    def __init__(self, x: int, z: int) -> None:
        self.chunk_x = x
        self.chunk_z = z
        self.chunk_data = [ChunkSection() for _ in range(24)]

    def get_chunk_data(self) -> bytes:
        buf = bytearray()
        for section in self.chunk_data:
            buf.extend(struct.pack(">h", section.get_non_air_count()))
            buf.extend(section.encode_block_container())
            buf.extend(section.encode_biome_container())

        return bytes(buf)

    def get_light_data(self) -> LightDataStruct:
        section_index = (-64 >> 4) + 4

        sky_mask = 1 << section_index
        block_mask = 1 << section_index

        full_light = [0xFF] * 2048

        return LightDataStruct(
            sky_y_mask=[sky_mask],
            block_y_mask=[block_mask],
            empty_sky_y_mask=[0],
            empty_block_y_mask=[0],
            sky_updates=[full_light],
            block_updates=[full_light],
        )

    def get_block(self, x: int, y: int, z: int) -> int:
        return self.get_section_for_y(y).get_block(x & 0xF, y & 0xF, z & 0xF)

    def set_block(self, x: int, y: int, z: int, block_data: int) -> None:
        self.get_section_for_y(y).set_block(
            x & 0xF, y & 0xF, z & 0xF, block_data
        )

    def get_section_for_y(self, world_y: int) -> ChunkSection:
        if not (MIN_WORLD_HEIGHT <= world_y <= MAX_WORLD_HEIGHT):
            raise ChunkSectionOutOfBoundsError(world_y=world_y)
        return self.chunk_data[(world_y >> 4) + 4]


class IWorldGenerator(Protocol):
    """Interface for terrain generators."""

    def generate_chunk(self, x: int, z: int) -> Chunk: ...
