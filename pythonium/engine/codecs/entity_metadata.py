from typing import Any

from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import (
    PositionCodec,
    StringCodec,
    TextComponentCodec,
    UUIDCodec,
    VarIntCodec,
    VarLongCodec,
)
from pythonium.engine.codecs.identifier import IdentifierCodec
from pythonium.engine.codecs.nbt import NBTCodec
from pythonium.engine.codecs.optional import OptionalCodec
from pythonium.engine.codecs.particle import ParticleDataCodec
from pythonium.engine.codecs.primitives import (
    BooleanCodec,
    ByteCodec,
    FloatCodec,
    UnsignedByteCodec,
)
from pythonium.engine.codecs.slot import SlotCodec
from pythonium.engine.exceptions import DecodeError, EncodeError
from pythonium.engine.typealiases import Deserialized


class FloatVector3Codec(Codec[tuple[float, float, float]]):
    """Codec for Rotations and Vector3 (3 floats)."""

    def __init__(self) -> None:
        self.float = FloatCodec()

    def serialize(self, *, field: tuple[float, float, float]) -> bytes:
        return b"".join(
            [
                self.float.serialize(field=field[0]),
                self.float.serialize(field=field[1]),
                self.float.serialize(field=field[2]),
            ]
        )

    def deserialize(
        self, data: bytes
    ) -> Deserialized[tuple[float, float, float]]:
        x, c1 = self.float.deserialize(data)
        y, c2 = self.float.deserialize(data[c1:])
        z, c3 = self.float.deserialize(data[c1 + c2 :])
        return (x, y, z), c1 + c2 + c3


class QuaternionCodec(Codec[tuple[float, float, float, float]]):
    """Codec for Quaternion (4 floats)."""

    def __init__(self) -> None:
        self.float = FloatCodec()

    def serialize(self, *, field: tuple[float, float, float, float]) -> bytes:
        return b"".join(
            [
                self.float.serialize(field=field[0]),
                self.float.serialize(field=field[1]),
                self.float.serialize(field=field[2]),
                self.float.serialize(field=field[3]),
            ]
        )

    def deserialize(
        self, data: bytes
    ) -> Deserialized[tuple[float, float, float, float]]:
        x, c1 = self.float.deserialize(data)
        y, c2 = self.float.deserialize(data[c1:])
        z, c3 = self.float.deserialize(data[c1 + c2 :])
        w, c4 = self.float.deserialize(data[c1 + c2 + c3 :])
        return (x, y, z, w), c1 + c2 + c3 + c4


class VillagerDataCodec(Codec[tuple[int, int, int]]):
    """Codec for Villager Data (3 VarInts)."""

    def __init__(self) -> None:
        self.varint = VarIntCodec()

    def serialize(self, *, field: tuple[int, int, int]) -> bytes:
        return b"".join(
            [
                self.varint.serialize(field=field[0]),
                self.varint.serialize(field=field[1]),
                self.varint.serialize(field=field[2]),
            ]
        )

    def deserialize(self, data: bytes) -> Deserialized[tuple[int, int, int]]:
        t, c1 = self.varint.deserialize(data)
        p, c2 = self.varint.deserialize(data[c1:])
        l, c3 = self.varint.deserialize(data[c1 + c2 :])
        return (t, p, l), c1 + c2 + c3


class OptionalGlobalPositionCodec(
    Codec[tuple[str, tuple[int, int, int]] | None]
):
    """Codec for Optional Global Position."""

    def __init__(self) -> None:
        self.boolean = BooleanCodec()
        self.identifier = IdentifierCodec()
        self.position = PositionCodec()

    def serialize(
        self, *, field: tuple[str, tuple[int, int, int]] | None
    ) -> bytes:
        if field is None:
            return self.boolean.serialize(field=False)
        return (
            self.boolean.serialize(field=True)
            + self.identifier.serialize(field=field[0])
            + self.position.serialize(field=field[1])
        )

    def deserialize(
        self, data: bytes
    ) -> Deserialized[tuple[str, tuple[int, int, int]] | None]:
        present, c1 = self.boolean.deserialize(data)
        if not present:
            return None, c1
        id_, c2 = self.identifier.deserialize(data[c1:])
        pos, c3 = self.position.deserialize(data[c1 + c2 :])
        return (id_, pos), c1 + c2 + c3


class OptionalVarIntSpecialCodec(Codec[int | None]):
    """Codec for Optional VarInt (0 for absent, value + 1 otherwise)."""

    def __init__(self) -> None:
        self.varint = VarIntCodec()

    def serialize(self, *, field: int | None) -> bytes:
        if field is None:
            return self.varint.serialize(field=0)
        return self.varint.serialize(field=field + 1)

    def deserialize(self, data: bytes) -> Deserialized[int | None]:
        val, c = self.varint.deserialize(data)
        if val == 0:
            return None, c
        return val - 1, c


class OptionalBlockStateCodec(Codec[int | None]):
    """Codec for Optional Block State (0 for absent, block state ID otherwise)."""

    def __init__(self) -> None:
        self.varint = VarIntCodec()

    def serialize(self, *, field: int | None) -> bytes:
        if field is None:
            return self.varint.serialize(field=0)
        return self.varint.serialize(field=field)

    def deserialize(self, data: bytes) -> Deserialized[int | None]:
        val, c = self.varint.deserialize(data)
        if val == 0:
            return None, c
        return val, c


class EntityMetadataCodec(Codec[dict[int, tuple[int, Any]]]):
    """Codec for Entity Metadata format."""

    def __init__(self) -> None:
        self.ubyte = UnsignedByteCodec()
        self.varint = VarIntCodec()

        self.codecs: dict[int, Codec] = {
            0: ByteCodec(),
            1: VarIntCodec(),
            2: VarLongCodec(),
            3: FloatCodec(),
            4: StringCodec(),
            5: TextComponentCodec(),
            6: OptionalCodec(TextComponentCodec()),
            7: SlotCodec(),
            8: BooleanCodec(),
            9: FloatVector3Codec(),
            10: PositionCodec(),
            11: OptionalCodec(PositionCodec()),
            12: VarIntCodec(),
            13: OptionalCodec(UUIDCodec()),
            14: VarIntCodec(),
            15: OptionalBlockStateCodec(),
            16: NBTCodec(),
            17: ParticleDataCodec(),
            18: ArrayCodec(ParticleDataCodec()),
            19: VillagerDataCodec(),
            20: OptionalVarIntSpecialCodec(),
            21: VarIntCodec(),
            22: VarIntCodec(),
            23: VarIntCodec(),
            24: VarIntCodec(),
            25: OptionalGlobalPositionCodec(),
            26: VarIntCodec(),
            27: VarIntCodec(),
            28: VarIntCodec(),
            29: FloatVector3Codec(),
            30: QuaternionCodec(),
        }

    def serialize(self, *, field: dict[int, tuple[int, Any]]) -> bytes:
        out = bytearray()
        for index, (type_id, value) in field.items():
            if index > 254 or index < 0:
                raise EncodeError(
                    info=f"Metadata index out of bounds: {index}"
                )
            out.extend(self.ubyte.serialize(field=index))
            out.extend(self.varint.serialize(field=type_id))

            codec = self.codecs.get(type_id)
            if not codec:
                raise EncodeError(info=f"Unknown metadata type ID: {type_id}")

            out.extend(codec.serialize(field=value))

        out.extend(self.ubyte.serialize(field=255))
        return bytes(out)

    def deserialize(
        self, data: bytes
    ) -> Deserialized[dict[int, tuple[int, Any]]]:
        offset = 0
        result = {}

        while offset < len(data):
            index, c1 = self.ubyte.deserialize(data[offset:])
            offset += c1

            if index == 255:
                break

            type_id, c2 = self.varint.deserialize(data[offset:])
            offset += c2

            codec = self.codecs.get(type_id)
            if not codec:
                raise DecodeError(info=f"Unknown metadata type ID: {type_id}")

            value, c3 = codec.deserialize(data[offset:])
            offset += c3

            result[index] = (type_id, value)

        return result, offset
