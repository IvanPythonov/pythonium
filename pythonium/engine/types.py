from typing import Annotated

from pythonium.engine.codecs import (
    BooleanCodec,
    ByteCodec,
    DoubleCodec,
    FloatCodec,
    IntCodec,
    LongCodec,
    ShortCodec,
    StringCodec,
    UnsignedByteCodec,
    UnsignedShortCodec,
    VarIntCodec,
    VarLongCodec,
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

type Boolean = Annotated[bool, BooleanCodec()]
