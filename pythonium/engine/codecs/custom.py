from typing import Final
from uuid import UUID

from msgspec.json import encode

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.nbt import NBTCodec
from pythonium.engine.codecs.primitives import DoubleCodec, LongCodec
from pythonium.engine.exceptions import (
    DecodeError,
    EncodeError,
    VarIntDecodeError,
    VarIntEncodeError,
)
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
        if not (-(2**31) <= field < 2**31):
            raise VarIntEncodeError(value=field, out_of_bounds=True)

        value = field & 0xFFFFFFFF
        out = bytearray()
        bytes_encountered = 0

        while True:
            temp = value & 0x7F
            value >>= 7

            if value != 0:
                temp |= 0x80

            out.append(temp)
            bytes_encountered += 1

            if bytes_encountered > self.__max_bytes__:
                raise VarIntEncodeError(
                    bytes_encountered=bytes_encountered,
                    max_bytes=self.__max_bytes__,
                )

            if value == 0:
                break

        return bytes(out)

    def deserialize(self, data: bytes) -> Deserialized[int]:
        number = 0
        bytes_encountered = 0

        for byte in data:
            number |= (byte & 0x7F) << (7 * bytes_encountered)
            bytes_encountered += 1

            if bytes_encountered > self.__max_bytes__:
                raise VarIntDecodeError(
                    bytes_encountered=bytes_encountered,
                    max_bytes=self.__max_bytes__,
                )

            if not (byte & 0x80):
                break
        else:
            raise VarIntDecodeError(
                bytes_encountered=bytes_encountered,
                max_bytes=self.__max_bytes__,
            )
        if number & (1 << 31):
            number -= 1 << 32

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
        z = (value >> 12) & 0x3FFFFFF
        y = value & 0xFFF

        if y >= 1 << 11:
            y -= 4096
        if x >= 1 << 25:
            x -= 67108864

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


class FixedByteArrayCodec(Codec[bytes]):
    """Codec for Fixed Byte Array."""

    def __init__(self, length: int) -> None:
        self.length = length

    def serialize(self, *, field: bytes) -> bytes:
        if len(field) != self.length:
            raise EncodeError(
                info=f"Expected {self.length} bytes, got {len(field)}"
            )
        return field

    def deserialize(self, data: bytes) -> Deserialized[bytes]:
        if len(data) < self.length:
            raise DecodeError(data=data)
        return data[: self.length], self.length


class DoubleVectorCodec(Codec[tuple[float, float, float]]):
    """Codec for a 3D Double Vector (X, Y, Z)."""

    def __init__(self) -> None:
        self.double_codec = DoubleCodec()

    def serialize(self, *, field: tuple[float, float, float]) -> bytes:
        x, y, z = field
        return b"".join(
            [
                self.double_codec.serialize(field=x),
                self.double_codec.serialize(field=y),
                self.double_codec.serialize(field=z),
            ]
        )

    def deserialize(
        self, data: bytes
    ) -> Deserialized[tuple[float, float, float]]:
        x, c1 = self.double_codec.deserialize(data)
        y, c2 = self.double_codec.deserialize(data[c1:])
        z, c3 = self.double_codec.deserialize(data[c1 + c2 :])
        return (x, y, z), c1 + c2 + c3


class PrefixedByteArrayCodec(Codec[bytes]):
    """Codec for a byte array prefixed with its length as a VarInt."""

    def serialize(self, *, field: bytes) -> bytes:
        return VarIntCodec().serialize(field=len(field)) + field

    def deserialize(self, data: bytes) -> Deserialized[bytes]:
        length, offset = VarIntCodec().deserialize(data)
        return data[offset : offset + length], offset + length


class PrefixedLongByteArrayCodec(Codec[bytes]):
    """Codec for a byte array prefixed with its length as a VarInt."""

    def serialize(self, *, field: bytes) -> bytes:
        return VarIntCodec().serialize(field=len(field)) + field

    def deserialize(self, data: bytes) -> Deserialized[bytes]:
        byte_len, offset = VarIntCodec().deserialize(data)
        return data[offset : offset + byte_len], offset + byte_len
