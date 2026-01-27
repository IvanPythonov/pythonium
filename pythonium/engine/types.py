from typing import Annotated

from pythonium.engine.codecs import (
    BooleanCodec,
    ByteCodec,
    DoubleCodec,
    FloatCodec,
    IntCodec,
    LongCodec,
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

type NBT = Annotated[dict, NBTCodec()]

type NBT_Byte = Annotated[int, NBT_Byte_Codec()]
type NBT_Short = Annotated[int, NBT_Short_Codec()]
type NBT_Int = Annotated[int, NBT_Int_Codec()]
type NBT_Long = Annotated[int, NBT_Long_Codec()]
type NBT_Float = Annotated[float, NBT_Float_Codec()]
type NBT_Double = Annotated[float, NBT_Double_Codec()]
type NBT_ByteArray = Annotated[list[int], NBT_Byte_Array_Codec()]
type NBT_String = Annotated[str, NBT_String_Codec()]
type NBT_List = Annotated[list, NBT_List_Codec()]
type NBT_Compound = Annotated[dict, NBT_Compound_Codec()]
type NBT_IntArray = Annotated[list[int], NBT_Int_Array_Codec()]
type NBT_LongArray = Annotated[list[int], NBT_Long_Array_Codec()]
type NBTString = Annotated[str, NBT_String_Codec()]

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
