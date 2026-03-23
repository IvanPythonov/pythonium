from msgspec import Struct

from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import StringCodec, VarIntCodec
from pythonium.engine.typealiases import Deserialized


class PropertySetStruct(Struct):
    """Property set struct."""

    property_set_id: str
    items: list[int]


class PropertySetCodec(Codec[PropertySetStruct]):
    """Property set codec."""

    def __init__(self) -> None:
        self.string = StringCodec()
        self.varint_array: ArrayCodec = ArrayCodec(VarIntCodec())

    def serialize(self, *, field: PropertySetStruct) -> bytes:
        return self.string.serialize(
            field=field.property_set_id
        ) + self.varint_array.serialize(field=field.items)

    def deserialize(self, data: bytes) -> Deserialized[PropertySetStruct]:
        pid, c1 = self.string.deserialize(data)
        items, c2 = self.varint_array.deserialize(data[c1:])
        return PropertySetStruct(pid, items), c1 + c2


class SlotDisplayStruct(Struct):
    """Slot display struct."""

    display_type: int
    data: bytes


class SlotDisplayCodec(Codec[SlotDisplayStruct]):
    """Slot display codec."""

    def __init__(self) -> None:
        self.varint = VarIntCodec()

    def serialize(self, *, field: SlotDisplayStruct) -> bytes:
        return self.varint.serialize(field=field.display_type) + field.data

    def deserialize(self, data: bytes) -> Deserialized[SlotDisplayStruct]:
        display_type, c1 = self.varint.deserialize(data)
        return SlotDisplayStruct(display_type, b""), c1


class StonecutterRecipeStruct(Struct):
    """Stonecutter recipe struct."""

    ingredients: list[int]
    slot_display: SlotDisplayStruct


class StonecutterRecipeCodec(Codec[StonecutterRecipeStruct]):
    """Stonecutter recipe codec."""

    def __init__(self) -> None:
        self.varint_array: ArrayCodec = ArrayCodec(VarIntCodec())
        self.slot_display = SlotDisplayCodec()

    def serialize(self, *, field: StonecutterRecipeStruct) -> bytes:
        return self.varint_array.serialize(
            field=field.ingredients
        ) + self.slot_display.serialize(field=field.slot_display)

    def deserialize(
        self, data: bytes
    ) -> Deserialized[StonecutterRecipeStruct]:
        ingredients, c1 = self.varint_array.deserialize(data)
        slot_display, c2 = self.slot_display.deserialize(data[c1:])
        return StonecutterRecipeStruct(ingredients, slot_display), c1 + c2
