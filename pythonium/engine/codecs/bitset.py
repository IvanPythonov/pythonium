from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.primitives import LongCodec
from pythonium.engine.typealiases import Deserialized


class BitSetCodec(Codec[list[int]]):
    """Codec for BitSet."""

    def __init__(self) -> None:
        self.array_codec: ArrayCodec = ArrayCodec(LongCodec())

    def serialize(self, *, field: list[int]) -> bytes:
        return self.array_codec.serialize(field=field)

    def deserialize(self, data: bytes) -> Deserialized[list[int]]:
        return self.array_codec.deserialize(data)
