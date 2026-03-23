from pythonium.engine.codecs.base import Codec
from pythonium.engine.typealiases import Deserialized


class RestBufferCodec(Codec[bytes]):
    """Codec for reading the remainderr of the packet buffer."""

    def serialize(self, *, field: bytes) -> bytes:
        return field

    def deserialize(self, data: bytes) -> Deserialized[bytes]:
        length = len(data)
        return data, length
