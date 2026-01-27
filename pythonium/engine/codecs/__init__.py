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
    NBT_Byte_Array_Codec,
    NBT_Byte_Codec,
    NBT_Compound_Codec,
    NBT_Double_Codec,
    NBT_Float_Codec,
    NBT_Int_Array_Codec,
    NBT_Int_Codec,
    NBT_List_Codec,
    NBT_Long_Array_Codec,
    NBT_Long_Codec,
    NBT_Short_Codec,
    NBT_String_Codec,
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
    "NBT_Byte_Array_Codec",
    "NBT_Byte_Codec",
    "NBT_Compound_Codec",
    "NBT_Double_Codec",
    "NBT_Float_Codec",
    "NBT_Int_Array_Codec",
    "NBT_Int_Codec",
    "NBT_List_Codec",
    "NBT_Long_Array_Codec",
    "NBT_Long_Codec",
    "NBT_Short_Codec",
    "NBT_String_Codec",
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
