"""Docstring for pythonium.engine.codecs."""

from .array import ArrayCodec
from .base import Codec, PrimitiveCodec, resolve_codec
from .custom import (
    PositionCodec,
    StringCodec,
    UUIDCodec,
    VarIntCodec,
    VarLongCodec,
)
from .nbt import (
    NBTCodec,
)
from .optional import OptionalCodec
from .primitives import (
    BooleanCodec,
    ByteCodec,
    DoubleCodec,
    FloatCodec,
    IntCodec,
    LongCodec,
    ShortCodec,
    UnsignedByteCodec,
    UnsignedShortCodec,
)

__all__ = (
    "ArrayCodec",
    "ArrayCodec",
    "BooleanCodec",
    "ByteCodec",
    "Codec",
    "DoubleCodec",
    "FloatCodec",
    "IntCodec",
    "LongCodec",
    "NBTCodec",
    "OptionalCodec",
    "PositionCodec",
    "PrimitiveCodec",
    "ShortCodec",
    "StringCodec",
    "UUIDCodec",
    "UnsignedByteCodec",
    "UnsignedShortCodec",
    "VarIntCodec",
    "VarLongCodec",
    "resolve_codec",
)
