from typing import Annotated

from pythonium.engine.codecs import (
    BooleanCodec,
    ByteCodec,
    DoubleCodec,
    FloatCodec,
    IntCodec,
    LongCodec,
    PositionCodec,
    ShortCodec,
    StringCodec,
    UnsignedByteCodec,
    UnsignedShortCodec,
    UUIDCodec,
    VarIntCodec,
    VarLongCodec,
)
from pythonium.engine.codecs.array import (
    BooleanArrayCodec,
    ByteArrayCodec,
    DoubleArrayCodec,
    FloatArrayCodec,
    IntArrayCodec,
    LongArrayCodec,
    ShortArrayCodec,
    StringArrayCodec,
    UnsignedByteArrayCodec,
    UnsignedShortArrayCodec,
    UUIDArrayCodec,
    VarIntArrayCodec,
    VarLongArrayCodec,
)

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

type ByteArray = Annotated[list[int], ByteArrayCodec()]
type UByteArray = Annotated[list[int], UnsignedByteArrayCodec()]

type ShortArray = Annotated[list[int], ShortArrayCodec()]
type UShortArray = Annotated[list[int], UnsignedShortArrayCodec()]

type IntArray = Annotated[list[int], IntArrayCodec()]
type LongArray = Annotated[list[int], LongArrayCodec()]

type FloatArray = Annotated[list[float], FloatArrayCodec()]
type DoubleArray = Annotated[list[float], DoubleArrayCodec()]

type StringArray = Annotated[list[str], StringArrayCodec()]

type UUIDArray = Annotated[list[str], UUIDArrayCodec()]

type BooleanArray = Annotated[list[bool], BooleanArrayCodec()]

type VarIntArray = Annotated[list[int], VarIntArrayCodec()]
type VarLongArray = Annotated[list[int], VarLongArrayCodec()]

type Position = Annotated[tuple[int, int, int], PositionCodec()]
