from pythonium.engine.codecs.base import ArrayCodec
from pythonium.engine.codecs.custom import (
    StringCodec,
    UUIDCodec,
    VarIntCodec,
    VarLongCodec,
)
from pythonium.engine.codecs.primitive import (
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


class BooleanArrayCodec(ArrayCodec[bool]):
    """Array of boolean values."""

    __element_codec__ = BooleanCodec()


class ByteArrayCodec(ArrayCodec[int]):
    """Array of signed byte values."""

    __element_codec__ = ByteCodec()


class UnsignedByteArrayCodec(ArrayCodec[int]):
    """Array of unsigned byte values."""

    __element_codec__ = UnsignedByteCodec()


class ShortArrayCodec(ArrayCodec[int]):
    """Array of signed short values."""

    __element_codec__ = ShortCodec()


class UnsignedShortArrayCodec(ArrayCodec[int]):
    """Array of unsigned short values."""

    __element_codec__ = UnsignedShortCodec()


class IntArrayCodec(ArrayCodec[int]):
    """Array of signed int values."""

    __element_codec__ = IntCodec()


class LongArrayCodec(ArrayCodec[int]):
    """Array of signed long values."""

    __element_codec__ = LongCodec()


class FloatArrayCodec(ArrayCodec[float]):
    """Array of float values."""

    __element_codec__ = FloatCodec()


class DoubleArrayCodec(ArrayCodec[float]):
    """Array of double values."""

    __element_codec__ = DoubleCodec()


class StringArrayCodec(ArrayCodec[str]):
    """Array of string values."""

    __element_codec__ = StringCodec()


class VarIntArrayCodec(ArrayCodec[int]):
    """Array of VarInt values."""

    __element_codec__ = VarIntCodec()


class VarLongArrayCodec(ArrayCodec[int]):
    """Array of VarLong values."""

    __element_codec__ = VarLongCodec()


class UUIDArrayCodec(ArrayCodec[str]):
    """Array of UUID values."""

    __element_codec__ = UUIDCodec()
