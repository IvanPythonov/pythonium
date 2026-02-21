from collections.abc import Sequence

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import VarIntCodec
from pythonium.engine.typealiases import Deserialized


class ArrayCodec[T](Codec[list[T]]):
    def __init__(
        self,
        element_codec: Codec | Sequence[Codec],
        length_codec: Codec | None = None,
    ) -> None:
        self.length_codec = length_codec or VarIntCodec()

        if isinstance(element_codec, (list, tuple)):
            self.codecs = element_codec
            self.single = None
        else:
            self.codecs = None
            self.single = element_codec

    def serialize(self, field: list[T]) -> bytes:
        chunks = [self.length_codec.serialize(field=len(field))]

        if self.codecs:
            for item in field:
                for codec, sub_item in zip(self.codecs, item, strict=False):
                    chunks.append(codec.serialize(field=sub_item))
        else:
            for item in field:
                chunks.append(self.single.serialize(field=item))

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
                result.append(tuple(row))
            else:
                val, consumed = self.single.deserialize(data[offset:])
                result.append(val)
                offset += consumed

        return result, offset
