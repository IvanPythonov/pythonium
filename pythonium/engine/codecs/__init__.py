"""Docstring for pythonium.engine.codecs."""

from .base import Codec, PrimitiveCodec, resolve_codec
from .custom import StringCodec, VarIntCodec, VarLongCodec
from .primitive import (
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
    "BooleanCodec",
    "ByteCodec",
    "Codec",
    "DoubleCodec",
    "FloatCodec",
    "IntCodec",
    "LongCodec",
    "PrimitiveCodec",
    "ShortCodec",
    "StringCodec",
    "UnsignedByteCodec",
    "UnsignedShortCodec",
    "VarIntCodec",
    "VarLongCodec",
    "resolve_codec",
)
