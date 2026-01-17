from typing import Any, Final

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import VarIntCodec
from pythonium.engine.typealiases import Deserialized


class ArrayCodec[T](Codec[list[T]]):
    """Codec for arrays prefixed with length."""

    def __init__(
        self,
        element_codec: Codec[T],
        length_codec: Codec[int] | None = None,
    ) -> None:
        self._element_codec: Final[Codec[Any]] = element_codec
        self._length_codec: Final[Codec[Any] | None] = length_codec

    def serialize(self, *, field: list[T]) -> bytes:
        length_codec = self._length_codec or VarIntCodec()
        length_bytes = length_codec.serialize(field=len(field))
        element_bytes = b"".join(
            self._element_codec.serialize(field=item) for item in field
        )
        return length_bytes + element_bytes

    def deserialize(self, data: bytes) -> Deserialized[list[T]]:
        length_codec = self._length_codec or VarIntCodec()
        length, offset = length_codec.deserialize(data)
        result: list[T] = []

        for _ in range(length):
            item, consumed = self._element_codec.deserialize(data[offset:])
            result.append(item)
            offset += consumed

        return result, offset
