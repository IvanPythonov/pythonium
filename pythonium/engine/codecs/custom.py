import struct

from pythonium.engine.codecs import Codec
from pythonium.engine.typealiases import Deserialized

SEGMENT_BITS = 0x7F
CONTINUE_BIT = 0x80


class StringCodec(Codec[str]):
    """
    String type implementation with Minecraft protocol serialization.

    UTF-8 string prefixed with its size in bytes as a VarInt. Maximum length of
    n characters, which varies by context.
    The encoding used on the wire is regular UTF-8, not Java's
    "slight modification". However, the length of the string for purposes of
    the length limit is its number of UTF-16 code units, that is,
    scalar values > U+FFFF are counted as two. Up to n * 3 bytes can be used to
    encode a UTF-8 string comprising n code units when converted to UTF-16,
    and both of those limits are checked. Maximum n value is 32767. The + 3 is
    due to the max size of a valid length VarInt.
    """

    def serialize(self, field: str) -> bytes:
        return VarIntCodec().serialize(field=len(field)) + field.encode(
            "utf-8"
        )

    def deserialize(self, data: bytes) -> Deserialized[str]:
        length, varint_size = VarIntCodec().deserialize(data)
        value = data[varint_size : varint_size + length].decode("utf-8")
        return value, varint_size + length


class VarIntCodec(Codec[int]):
    """
    VarInt type implementation with Minecraft protocol serialization.

    Variable-length data encoding a two's complement signed 32-bit integer.
    """

    __max_bytes__ = 5

    def serialize(self, field: int) -> bytes:
        out = b""
        bytes_encountered = 0

        while True:
            byte = field & SEGMENT_BITS
            field >>= 7
            out += struct.pack("B", byte | (CONTINUE_BIT if field > 0 else 0))
            if field == 0:
                break
            bytes_encountered += 1
            if bytes_encountered > self.__max_bytes__:
                msg = "Tried to read too long of a VarInt"
                raise ValueError(msg)
        return out

    def deserialize(self, data: bytes) -> Deserialized[int]:
        number = 0
        bytes_encountered = 0

        for byte in data:
            number |= (byte & SEGMENT_BITS) << 7 * bytes_encountered
            bytes_encountered += 1
            if not byte & CONTINUE_BIT:
                break

            if bytes_encountered > self.__max_bytes__:
                msg = "Tried to read too long of a VarInt"
                raise ValueError(msg)
        return number, bytes_encountered


class VarLongCodec(VarIntCodec):
    """
    VarLong type implementation with Minecraft protocol serialization.

    Variable-length data encoding a two's complement signed 64-bit integer.
    """

    __max_bytes__ = 10
