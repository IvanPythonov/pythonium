from typing import Annotated

from nbtlib import Base as BaseTag

from pythonium.engine.codecs import (
    BooleanCodec,
    ByteCodec,
    DoubleCodec,
    FloatCodec,
    IntCodec,
    LongCodec,
    NBTCodec,
    PositionCodec,
    ShortCodec,
    StringCodec,
    UnsignedByteCodec,
    UnsignedShortCodec,
    UUIDCodec,
    VarIntCodec,
    VarLongCodec,
)
from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.optional import OptionalCodec

type VarInt = Annotated[int, VarIntCodec()]
type VarLong = Annotated[int, VarLongCodec()]

type Byte = Annotated[int, ByteCodec()]
type UByte = Annotated[int, UnsignedByteCodec()]

type Short = Annotated[int, ShortCodec()]
type UShort = Annotated[int, UnsignedShortCodec()]

type Int = Annotated[int, IntCodec()]
type Long = Annotated[int, LongCodec()]

type Float = Annotated[float, FloatCodec()]
type Double = Annotated[float, DoubleCodec()]

type String = Annotated[str, StringCodec()]
type UUID = Annotated[str, UUIDCodec()]
type Boolean = Annotated[bool, BooleanCodec()]

type Position = Annotated[tuple[int, int, int], PositionCodec()]

type ByteArray = Annotated[list[int], ArrayCodec(ByteCodec())]
type UByteArray = Annotated[list[int], ArrayCodec(UnsignedByteCodec())]

type ShortArray = Annotated[list[int], ArrayCodec(ShortCodec())]
type UShortArray = Annotated[list[int], ArrayCodec(UnsignedShortCodec())]

type IntArray = Annotated[list[int], ArrayCodec(IntCodec())]
type LongArray = Annotated[list[int], ArrayCodec(LongCodec())]

type FloatArray = Annotated[list[float], ArrayCodec(FloatCodec())]
type DoubleArray = Annotated[list[float], ArrayCodec(DoubleCodec())]

type StringArray = Annotated[list[str], ArrayCodec(StringCodec())]
type UUIDArray = Annotated[list[str], ArrayCodec(UUIDCodec())]
type BooleanArray = Annotated[list[bool], ArrayCodec(BooleanCodec())]

type VarIntArray = Annotated[list[int], ArrayCodec(VarIntCodec())]
type VarLongArray = Annotated[list[int], ArrayCodec(VarLongCodec())]

type OptionalString = Annotated[str | None, OptionalCodec(StringCodec())]
type OptionalVarInt = Annotated[int | None, OptionalCodec(VarIntCodec())]
type OptionalUUID = Annotated[str | None, OptionalCodec(UUIDCodec())]
type OptionalBoolean = Annotated[bool | None, OptionalCodec(BooleanCodec())]
type OptionalPosition = Annotated[
    tuple[int, int, int] | None, OptionalCodec(PositionCodec())
]
type OptionalNBT = Annotated[
    dict[str, BaseTag] | None, OptionalCodec(NBTCodec())
]

type NBTCompound = Annotated[dict[str, BaseTag], NBTCodec()]

type Identifier = Annotated[
    str, StringCodec()
]  # TODO(IvanPythonov): Create IdentifierCodec WITH VALIDATION  # noqa: FIX002
