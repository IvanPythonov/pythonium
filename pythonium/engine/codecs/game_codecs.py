from msgspec import Struct

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import StringCodec
from pythonium.engine.codecs.primitives import ByteCodec, DoubleCodec
from pythonium.engine.typealiases import Deserialized


class ModifierDataStruct(Struct):
    """Structure representing a single Attribute Modifier."""

    id: str  # Identifier (e.g. 'minecraft:movement_speed')
    amount: float  # Double
    operation: int  # Byte (0, 1, or 2)


class ModifierDataCodec(Codec[ModifierDataStruct]):
    """Codec for Attribute Modifier Data."""

    def __init__(self) -> None:
        self.string_codec = StringCodec()
        self.double_codec = DoubleCodec()
        self.byte_codec = ByteCodec()

    def serialize(self, *, field: ModifierDataStruct) -> bytes:
        return b"".join(
            [
                self.string_codec.serialize(field=field.id),
                self.double_codec.serialize(field=field.amount),
                self.byte_codec.serialize(field=field.operation),
            ]
        )

    def deserialize(self, data: bytes) -> Deserialized[ModifierDataStruct]:
        mod_id, c1 = self.string_codec.deserialize(data)
        amount, c2 = self.double_codec.deserialize(data[c1:])
        operation, c3 = self.byte_codec.deserialize(data[c1 + c2 :])

        return ModifierDataStruct(
            id=mod_id, amount=amount, operation=operation
        ), c1 + c2 + c3
