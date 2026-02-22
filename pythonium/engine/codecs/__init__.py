"""Docstring for pythonium.engine.codecs."""

from .array import ArrayCodec
from .base import Codec, PrimitiveCodec, resolve_codec
from .custom import (
    PositionCodec,
    StringCodec,
    TextComponentCodec,
    UUIDCodec,
    VarIntCodec,
    VarLongCodec,
)
from .game_codecs import ModifierDataCodec, ModifierDataStruct
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
from .slot import SlotCodec

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
    "ModifierDataCodec",
    "ModifierDataStruct",
    "NBTCodec",
    "OptionalCodec",
    "PositionCodec",
    "PrimitiveCodec",
    "ShortCodec",
    "SlotCodec",
    "StringCodec",
    "TextComponentCodec",
    "UUIDCodec",
    "UnsignedByteCodec",
    "UnsignedShortCodec",
    "VarIntCodec",
    "VarLongCodec",
    "resolve_codec",
)
