from pythonium.engine.codecs import Codec
from pythonium.engine.typealiases import Deserialized


class Field[T]:
    """Class representing a field used in packets."""

    def __init__(
        self,
        name: str,
        codec: Codec[T],
    ) -> None:
        self.name = name

        self.codec = codec

    def serialize(self, value: T) -> bytes:
        return self.codec.serialize(value)

    def deserialize(self, data: bytes) -> Deserialized[T]:
        return self.codec.deserialize(data)
