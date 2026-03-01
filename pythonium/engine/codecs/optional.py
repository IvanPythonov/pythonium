from typing import Any, Final

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.primitives import BooleanCodec
from pythonium.engine.exceptions import DecodeError
from pythonium.engine.typealiases import Deserialized

_INTERNAL_BOOLEAN_CODEC = BooleanCodec()


class OptionalCodec[T](Codec[T | None]):
    """A field of type X, or nothing."""

    def __init__(self, inner_codec: Codec[T]) -> None:
        self.inner_codec: Final[Codec[Any]] = inner_codec

    def serialize(self, *, field: T | None) -> bytes:
        if field is None:
            return _INTERNAL_BOOLEAN_CODEC.serialize(field=False)

        return _INTERNAL_BOOLEAN_CODEC.serialize(
            field=True
        ) + self.inner_codec.serialize(field=field)

    def deserialize(self, data: bytes) -> Deserialized[T | None]:
        if not data:
            raise DecodeError(data=data)

        present = data[0] != 0
        offset = 1

        if present:
            value, consumed = self.inner_codec.deserialize(data[offset:])
            return value, offset + consumed

        return None, offset
