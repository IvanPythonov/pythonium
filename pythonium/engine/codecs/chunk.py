from msgspec import Struct

from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.bitset import BitSetCodec
from pythonium.engine.codecs.custom import VarIntCodec
from pythonium.engine.codecs.nbt import NBTCodec
from pythonium.engine.codecs.primitives import (
    ByteCodec,
    IntCodec,
    LongCodec,
    ShortCodec,
    UnsignedByteCodec,
)
from pythonium.engine.typealiases import Deserialized


class HeightmapsCodec(Codec[dict[str, list[int]]]):
    """Encodes Heightmaps as Network Map<String, LongArray>."""

    def __init__(self) -> None:
        self._HEIGHTMAP_TYPES = {
            "WORLD_SURFACE": 1,
            "MOTION_BLOCKING": 4,
            "MOTION_BLOCKING_NO_LEAVES": 5,
        }
        self._HEIGHTMAP_TYPES_BY_ID = {
            value: key for key, value in self._HEIGHTMAP_TYPES.items()
        }
        self.varint = VarIntCodec()
        self.long_array: ArrayCodec = ArrayCodec(LongCodec())

    def serialize(self, *, field: dict[str, list[int]]) -> bytes:
        out = bytearray()
        out.extend(self.varint.serialize(field=len(field)))

        for key, longs in field.items():
            out.extend(self.varint.serialize(field=self._HEIGHTMAP_TYPES[key]))
            out.extend(self.long_array.serialize(field=longs))

        return bytes(out)

    def deserialize(self, data: bytes) -> Deserialized[dict[str, list[int]]]:
        length, offset = self.varint.deserialize(data)
        result: dict[str, list[int]] = {}

        for _ in range(length):
            type_id, consumed = self.varint.deserialize(data[offset:])
            offset += consumed

            values, consumed = self.long_array.deserialize(data[offset:])
            offset += consumed

            result[self._HEIGHTMAP_TYPES_BY_ID[type_id]] = values

        return result, offset


class ChunkBiomeDataStruct(Struct):
    """Chunk biome data struct."""

    chunk_z: int
    chunk_x: int
    data: list[int]


class ChunkBiomeDataCodec(Codec[ChunkBiomeDataStruct]):
    """Chunk biome data codec."""

    def __init__(self) -> None:
        self.int_codec = IntCodec()

        self.byte_array_codec: ArrayCodec = ArrayCodec(ByteCodec())

    def serialize(self, *, field: ChunkBiomeDataStruct) -> bytes:
        return b"".join(
            [
                self.int_codec.serialize(field=field.chunk_z),
                self.int_codec.serialize(field=field.chunk_x),
                self.byte_array_codec.serialize(field=field.data),
            ]
        )

    def deserialize(self, data: bytes) -> Deserialized[ChunkBiomeDataStruct]:
        z, c1 = self.int_codec.deserialize(data)
        x, c2 = self.int_codec.deserialize(data[c1:])
        biome_data, c3 = self.byte_array_codec.deserialize(data[c1 + c2 :])

        return ChunkBiomeDataStruct(
            chunk_z=z, chunk_x=x, data=biome_data
        ), c1 + c2 + c3


class BlockEntityStruct(Struct):
    """Block entity struct."""

    packed_xz: int
    y: int
    type_: int
    data: dict | None = None  # NBTCompound


class BlockEntityCodec(Codec[BlockEntityStruct]):
    """Block entity codec."""

    def __init__(self) -> None:
        self.ubyte = UnsignedByteCodec()
        self.short = ShortCodec()
        self.varint = VarIntCodec()
        self.nbt = NBTCodec()

    def serialize(self, *, field: BlockEntityStruct) -> bytes:
        out = bytearray()
        out.extend(self.ubyte.serialize(field=field.packed_xz))
        out.extend(self.short.serialize(field=field.y))
        out.extend(self.varint.serialize(field=field.type_))
        if field.data:
            out.extend(self.nbt.serialize(field=field.data))
        else:
            out.extend(b"\x00")
        return bytes(out)

    def deserialize(self, data: bytes) -> Deserialized[BlockEntityStruct]:
        xz, c1 = self.ubyte.deserialize(data)
        y, c2 = self.short.deserialize(data[c1:])
        type_, c3 = self.varint.deserialize(data[c1 + c2 :])
        nbt_data, c4 = self.nbt.deserialize(data[c1 + c2 + c3 :])

        return BlockEntityStruct(xz, y, type_, nbt_data), c1 + c2 + c3 + c4


class LightDataStruct(Struct):
    """Light data struct."""

    sky_y_mask: list[int]
    block_y_mask: list[int]
    empty_sky_y_mask: list[int]
    empty_block_y_mask: list[int]
    sky_updates: list[list[int]]
    block_updates: list[list[int]]


class LightDataCodec(Codec[LightDataStruct]):
    """Light data codec."""

    def __init__(self) -> None:
        self.bitset = BitSetCodec()

        self.byte_array_array: ArrayCodec = ArrayCodec(
            ArrayCodec(UnsignedByteCodec())
        )

    def serialize(self, *, field: LightDataStruct) -> bytes:
        return b"".join(
            [
                self.bitset.serialize(field=field.sky_y_mask),
                self.bitset.serialize(field=field.block_y_mask),
                self.bitset.serialize(field=field.empty_sky_y_mask),
                self.bitset.serialize(field=field.empty_block_y_mask),
                self.byte_array_array.serialize(field=field.sky_updates),
                self.byte_array_array.serialize(field=field.block_updates),
            ]
        )

    def deserialize(self, data: bytes) -> Deserialized[LightDataStruct]:
        sym, c1 = self.bitset.deserialize(data)
        bym, c2 = self.bitset.deserialize(data[c1:])
        esym, c3 = self.bitset.deserialize(data[c1 + c2 :])
        ebym, c4 = self.bitset.deserialize(data[c1 + c2 + c3 :])
        su, c5 = self.byte_array_array.deserialize(data[c1 + c2 + c3 + c4 :])
        bu, c6 = self.byte_array_array.deserialize(
            data[c1 + c2 + c3 + c4 + c5 :]
        )

        return LightDataStruct(
            sym, bym, esym, ebym, su, bu
        ), c1 + c2 + c3 + c4 + c5 + c6
