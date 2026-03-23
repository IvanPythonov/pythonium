from msgspec import Struct
from nbtlib import Base as BaseTag

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import (
    StringCodec,
    TextComponentCodec,
    VarIntCodec,
)
from pythonium.engine.codecs.nbt import NBTCodec
from pythonium.engine.codecs.primitives import BooleanCodec, ByteCodec
from pythonium.engine.exceptions import EncodeError
from pythonium.engine.typealiases import Deserialized


class NumberFormatStruct(Struct):
    """Number format struct."""

    format_type: int
    styling: dict[str, BaseTag] | None = None
    content: dict | None = None


class NumberFormatCodec(Codec[NumberFormatStruct]):
    """Number format codec."""

    def __init__(self) -> None:
        self.varint = VarIntCodec()
        self.nbt = NBTCodec()
        self.text = TextComponentCodec()

    def serialize(self, *, field: NumberFormatStruct) -> bytes:
        out = bytearray(self.varint.serialize(field=field.format_type))
        if field.format_type == 1 and field.styling:
            out.extend(self.nbt.serialize(field=field.styling))
        elif field.format_type == 2 and field.content:
            out.extend(self.text.serialize(field=field.content))
        return bytes(out)

    def deserialize(self, data: bytes) -> Deserialized[NumberFormatStruct]:
        ftype, consumed = self.varint.deserialize(data)
        styling, content = None, None

        if ftype == 1:
            styling, c = self.nbt.deserialize(data[consumed:])
            consumed += c
        elif ftype == 2:
            content, c = self.text.deserialize(data[consumed:])
            consumed += c

        return NumberFormatStruct(ftype, styling, content), consumed


class ObjectiveDataStruct(Struct):
    """Objective data struct."""

    objective_value: dict | None = None
    type_: int | None = None
    number_format: NumberFormatStruct | None = None


class UpdateObjectiveStruct(Struct):
    """Update objective struct."""

    objective_name: str
    mode: int
    data: ObjectiveDataStruct | None = None


class UpdateObjectiveCodec(Codec[UpdateObjectiveStruct]):
    """Codec for Scoreboard Objectives."""

    def __init__(self) -> None:
        self.string = StringCodec()
        self.byte = ByteCodec()
        self.text = TextComponentCodec()
        self.varint = VarIntCodec()
        self.boolean = BooleanCodec()
        self.number_format = NumberFormatCodec()

    def serialize(self, *, field: UpdateObjectiveStruct) -> bytes:
        out = bytearray()
        out.extend(self.string.serialize(field=field.objective_name))
        out.extend(self.byte.serialize(field=field.mode))

        if (
            field.mode in (0, 2)
            and field.data.objective_value
            and field.data.type_
        ):
            if not field.data:
                raise EncodeError(
                    info="Objective data is required for mode 0 or 2"
                )
            out.extend(self.text.serialize(field=field.data.objective_value))
            out.extend(self.varint.serialize(field=field.data.type_))

            has_format = field.data.number_format is not None
            out.extend(self.boolean.serialize(field=has_format))
            if has_format and field.data.number_format:
                out.extend(
                    self.number_format.serialize(
                        field=field.data.number_format
                    )
                )

        return bytes(out)

    def deserialize(self, data: bytes) -> Deserialized[UpdateObjectiveStruct]:
        name, c1 = self.string.deserialize(data)
        mode, c2 = self.byte.deserialize(data[c1:])
        consumed = c1 + c2

        obj_data = None
        if mode in (0, 2):
            value, c3 = self.text.deserialize(data[consumed:])
            type_, c4 = self.varint.deserialize(data[consumed + c3 :])
            has_fmt, c5 = self.boolean.deserialize(data[consumed + c3 + c4 :])
            consumed += c3 + c4 + c5

            num_fmt = None
            if has_fmt:
                num_fmt, c6 = self.number_format.deserialize(data[consumed:])
                consumed += c6

            obj_data = ObjectiveDataStruct(value, type_, num_fmt)

        return UpdateObjectiveStruct(name, mode, obj_data), consumed
