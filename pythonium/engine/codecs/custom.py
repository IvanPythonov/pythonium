import struct
from typing import Final
from uuid import UUID

from msgspec.json import encode

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.nbt import NBTCodec
from pythonium.engine.codecs.primitives import LongCodec
from pythonium.engine.exceptions import DecodeError, VarIntDecodeError
from pythonium.engine.typealiases import Deserialized

SEGMENT_BITS: Final[int] = 0x7F
CONTINUE_BIT: Final[int] = 0x80

MAX_STRING_LENGTH: Final[int] = 65535


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

    def serialize(self, *, field: str) -> bytes:
        encoded_field = field.encode("utf-8")
        return (
            VarIntCodec().serialize(field=len(encoded_field)) + encoded_field
        )

    def deserialize(self, data: bytes) -> Deserialized[str]:
        length, varint_size = VarIntCodec().deserialize(data)
        if length > MAX_STRING_LENGTH:
            raise DecodeError(max_length=MAX_STRING_LENGTH, length=length)
        value = data[varint_size : varint_size + length].decode("utf-8")
        return value, varint_size + length


class VarIntCodec(Codec[int]):
    """
    VarInt type implementation with Minecraft protocol serialization.

    Variable-length data encoding a two's complement signed 32-bit integer.
    """

    __max_bytes__ = 5

    def serialize(self, *, field: int) -> bytes:
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
                raise VarIntDecodeError(
                    bytes_encountered=bytes_encountered,
                    max_bytes=self.__max_bytes__,
                )
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
                raise VarIntDecodeError(
                    bytes_encountered=bytes_encountered,
                    max_bytes=self.__max_bytes__,
                )
        return number, bytes_encountered


class VarLongCodec(VarIntCodec):
    """
    VarLong type implementation with Minecraft protocol serialization.

    Variable-length data encoding a two's complement signed 64-bit integer.
    """

    __max_bytes__ = 10


class UUIDCodec(Codec[str]):
    """
    UUID type implementation with Minecraft protocol serialization.

    UUID encoded as a two's complement signed 64-bit integer.
    """

    def serialize(self, *, field: str) -> bytes:
        return UUID(field).int.to_bytes(16, "big")

    def deserialize(self, data: bytes) -> Deserialized[str]:
        uuid_ = UUID(int=int.from_bytes(data[:16], "big"))
        return str(uuid_), 16


class PositionCodec(Codec[tuple[int, int, int]]):
    """
    Position type implementation with Minecraft protocol serialization.

    Encoded as a 64-bit integer where x, y, z coordinates are packed.
    """

    def serialize(self, *, field: tuple[int, int, int]) -> bytes:
        x, y, z = field
        return LongCodec().serialize(
            field=((x & 0x3FFFFFF) << 38)
            | ((z & 0x3FFFFFF) << 12)
            | (y & 0xFFF)
        )

    def deserialize(self, data: bytes) -> Deserialized[tuple[int, int, int]]:
        value, consumed = LongCodec().deserialize(data)

        x = value >> 38
        y = value << 52 >> 52
        z = value << 26 >> 38
        return (x, y, z), consumed


class TextComponentCodec(Codec[dict]):
    """
    Codec for Text Components.

    In protocol 772 (1.21.x), Text Components are serialized as Network NBT.
    """

    def serialize(self, *, field: dict) -> bytes:
        return NBTCodec().serialize(field=field)

    def deserialize(self, data: bytes) -> Deserialized[dict]:
        value, consumed = NBTCodec().deserialize(data)
        return value, consumed


class JsonTextComponentCodec(Codec[str]):
    """Codec for Json Text Components."""

    def serialize(self, *, field: str) -> bytes:
        return StringCodec().serialize(field=encode({"text": field}).decode())

    def deserialize(self, data: bytes) -> Deserialized[str]:
        return StringCodec().deserialize(data=data)
