from msgspec import Struct

from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import VarIntCodec
from pythonium.engine.codecs.optional import OptionalCodec
from pythonium.engine.codecs.primitives import ByteCodec
from pythonium.engine.typealiases import Deserialized


class RecipeDisplayStruct(Struct):
    """Struct for Recipe Display."""

    display_type: int
    data: bytes


class RecipeDisplayCodec(Codec[RecipeDisplayStruct]):
    """Recipe Display Codec."""

    def __init__(self) -> None:
        self.varint = VarIntCodec()

    def serialize(self, *, field: RecipeDisplayStruct) -> bytes:
        return self.varint.serialize(field=field.display_type) + field.data

    def deserialize(self, data: bytes) -> Deserialized[RecipeDisplayStruct]:
        display_type, consumed = self.varint.deserialize(data)

        return RecipeDisplayStruct(
            display_type=display_type, data=b""
        ), consumed


class RecipeStruct(Struct):
    """Struct representing Recipe."""

    recipe_id: int
    display: RecipeDisplayStruct
    group_id: int
    category_id: int
    ingredients: list[list[int]] | None
    flags: int


class RecipeCodec(Codec[RecipeStruct]):
    """Recipe codec."""

    def __init__(self) -> None:
        self.varint = VarIntCodec()
        self.display = RecipeDisplayCodec()
        self.byte = ByteCodec()

        self.ingredients: OptionalCodec = OptionalCodec(
            ArrayCodec(ArrayCodec(self.varint))
        )

    def serialize(self, *, field: RecipeStruct) -> bytes:
        return b"".join(
            [
                self.varint.serialize(field=field.recipe_id),
                self.display.serialize(field=field.display),
                self.varint.serialize(field=field.group_id),
                self.varint.serialize(field=field.category_id),
                self.ingredients.serialize(field=field.ingredients),
                self.byte.serialize(field=field.flags),
            ]
        )

    def deserialize(self, data: bytes) -> Deserialized[RecipeStruct]:
        recipe_id, c1 = self.varint.deserialize(data)
        display, c2 = self.display.deserialize(data[c1:])
        group_id, c3 = self.varint.deserialize(data[c1 + c2 :])
        category_id, c4 = self.varint.deserialize(data[c1 + c2 + c3 :])
        ingredients, c5 = self.ingredients.deserialize(
            data[c1 + c2 + c3 + c4 :]
        )
        flags, c6 = self.byte.deserialize(data[c1 + c2 + c3 + c4 + c5 :])

        return RecipeStruct(
            recipe_id=recipe_id,
            display=display,
            group_id=group_id,
            category_id=category_id,
            ingredients=ingredients,
            flags=flags,
        ), c1 + c2 + c3 + c4 + c5 + c6
