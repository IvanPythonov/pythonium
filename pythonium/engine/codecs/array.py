from collections.abc import Iterable, Sequence
from typing import Any, cast

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import VarIntCodec
from pythonium.engine.typealiases import Deserialized


class ArrayCodec[T](Codec[list[T]]):
    """Codec for list/array types."""

    def __init__(
        self,
        element_codec: Codec | Sequence[Codec],
        length_codec: Codec | None = None,
    ) -> None:
        self.length_codec = length_codec or VarIntCodec()

        self.codecs: Sequence[Codec] | None
        self.single: Codec | None

        if isinstance(element_codec, (list, tuple)):
            self.codecs = element_codec
            self.single = None
        else:
            self.codecs = None
            self.single = element_codec  # ignore: type[assignment]

    def serialize(self, field: list[T]) -> bytes:
        chunks = [self.length_codec.serialize(field=len(field))]

        if self.codecs:
            for item in field:
                iterable_item = cast("Iterable[Any]", item)

                for codec, sub_item in zip(
                    self.codecs, iterable_item, strict=False
                ):
                    chunks.append(codec.serialize(field=sub_item))
        elif self.single:
            chunks.extend(self.single.serialize(field=item) for item in field)

        return b"".join(chunks)

    def deserialize(self, data: bytes) -> Deserialized[list[T]]:
        length, offset = self.length_codec.deserialize(data)
        result = []

        for _ in range(length):
            if self.codecs:
                row = []
                for codec in self.codecs:
                    val, consumed = codec.deserialize(data[offset:])
                    row.append(val)
                    offset += consumed
                result.append(tuple(row))  # type: ignore[arg-type]
            elif self.single:
                val, consumed = self.single.deserialize(data[offset:])
                result.append(val)
                offset += consumed

        return result, offset  # type: ignore[return-value]
