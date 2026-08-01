from collections.abc import Iterable, Sequence
from typing import Any, cast

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import VarIntCodec
from pythonium.engine.typealiases import Deserialized


class ArrayCodec[T](Codec[list[T]]):
    """Aray codec."""

    def __init__(
        self,
        element_codec: Codec | Sequence[Codec],
        length_codec: Codec | None = None,
    ) -> None:
        self.length_codec = length_codec or VarIntCodec()

        self.codecs: Sequence[Codec] | None = None
        self.single: Codec | None = None

        if isinstance(element_codec, (list, tuple)):
            self.codecs = element_codec
        else:
            self.single = element_codec  # type: ignore[assignment]

    def serialize(self, field: list[T]) -> bytes:
        length_bytes = self.length_codec.serialize(field=len(field))

        if self.single:
            _serialize = self.single.serialize
            chunks = [_serialize(field=item) for item in field]

            return b"".join([length_bytes, *chunks])

        if self.codecs:
            chunks = [length_bytes]
            _append = chunks.append
            _codecs = self.codecs
            for item in field:
                iterable_item = cast("Iterable[Any]", item)
                for codec, sub_item in zip(
                    _codecs, iterable_item, strict=False
                ):
                    _append(codec.serialize(field=sub_item))
            return b"".join(chunks)

        return length_bytes

    def deserialize(self, data: bytes) -> Deserialized[list[T]]:
        length, offset = self.length_codec.deserialize(data)

        if length == 0:
            return [], offset

        result: list[T] = []
        _append = result.append

        if self.single:
            _deserialize = self.single.deserialize
            for _ in range(length):
                val, consumed = _deserialize(data[offset:])
                _append(val)
                offset += consumed
        elif self.codecs:
            _codecs = self.codecs
            for _ in range(length):
                row: list[Any] = []
                _row_append = row.append
                for codec in _codecs:
                    val, consumed = codec.deserialize(data[offset:])
                    _row_append(val)
                    offset += consumed
                _append(tuple(row))  # type: ignore[arg-type]

        return result, offset  # type: ignore[return-value]
