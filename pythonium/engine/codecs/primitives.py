from pythonium.engine.codecs.base import PrimitiveCodec


class BooleanCodec(PrimitiveCodec[bool]):
    """
    Boolean type implementation with Minecraft protocol serialization.

    True is encoded as 0x01, false as 0x00.
    """

    __format_character__ = "?"


class ByteCodec(PrimitiveCodec[int]):
    """
    Byte type implementation with Minecraft protocol serialization.

    Signed 8-bit integer, two's complement.
    """

    __format_character__ = ">b"


class UnsignedByteCodec(PrimitiveCodec[int]):
    """
    Unsigned Byte type implementation with Minecraft protocol serialization.

    Unsigned 8-bit integer.
    """

    __format_character__ = ">B"


class ShortCodec(PrimitiveCodec[int]):
    """
    Short type implementation with Minecraft protocol serialization.

    Signed 16-bit integer, two's complement.
    """

    __format_character__ = ">h"


class UnsignedShortCodec(PrimitiveCodec[int]):
    """
    Unsigned Short type implementation with Minecraft protocol serialization.

    Unsigned 16-bit integer.
    """

    __format_character__ = ">H"


class IntCodec(PrimitiveCodec[int]):
    """
    Int type implementation with Minecraft protocol serialization.

    Signed 32-bit integer, two's complement.
    """

    __format_character__ = ">i"


class LongCodec(PrimitiveCodec[int]):
    """
    Long type implementation with Minecraft protocol serialization.

    Signed 64-bit integer, two's complement.
    """

    __format_character__ = ">q"


class FloatCodec(PrimitiveCodec[float]):
    """
    Float type implementation with Minecraft protocol serialization.

    A single-precision 32-bit IEEE 754 floating point number
    """

    __format_character__ = ">f"


class DoubleCodec(PrimitiveCodec[float]):
    """
    Double type implementation with Minecraft protocol serialization.

    A double-precision 64-bit IEEE 754 floating point number.
    """

    __format_character__ = ">d"
