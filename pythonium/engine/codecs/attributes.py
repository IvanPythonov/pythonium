from msgspec import Struct

from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import VarIntCodec
from pythonium.engine.codecs.game_codecs import (
    ModifierDataCodec,
    ModifierDataStruct,
)
from pythonium.engine.codecs.primitives import DoubleCodec
from pythonium.engine.typealiases import Deserialized


class AttributePropertyStruct(Struct):
    """Struct representing AttributePropertyStruct."""

    id: int
    value: float
    modifiers: list[ModifierDataStruct]


class AttributePropertyCodec(Codec[AttributePropertyStruct]):
    """Codec for AttributePropertyCodec."""

    def __init__(self) -> None:
        self.varint = VarIntCodec()
        self.double = DoubleCodec()
        self.modifier_array: ArrayCodec = ArrayCodec(ModifierDataCodec())

    def serialize(self, *, field: AttributePropertyStruct) -> bytes:
        return b"".join(
            [
                self.varint.serialize(field=field.id),
                self.double.serialize(field=field.value),
                self.modifier_array.serialize(field=field.modifiers),
            ]
        )

    def deserialize(
        self, data: bytes
    ) -> Deserialized[AttributePropertyStruct]:
        prop_id, c1 = self.varint.deserialize(data)
        value, c2 = self.double.deserialize(data[c1:])
        modifiers, c3 = self.modifier_array.deserialize(data[c1 + c2 :])

        return AttributePropertyStruct(prop_id, value, modifiers), c1 + c2 + c3
