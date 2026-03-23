from msgspec import Struct

from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import TextComponentCodec, VarIntCodec
from pythonium.engine.codecs.optional import OptionalCodec
from pythonium.engine.codecs.primitives import ByteCodec, UnsignedByteCodec
from pythonium.engine.exceptions import EncodeError
from pythonium.engine.typealiases import Deserialized


class MapIconStruct(Struct):
    """Struct representing Map Icon."""

    type_: int
    x: int
    z: int
    direction: int
    display_name: dict | None


class MapIconCodec(Codec[MapIconStruct]):
    """Map Icon codec."""

    def __init__(self) -> None:
        self.varint = VarIntCodec()
        self.byte = ByteCodec()
        self.opt_text = OptionalCodec(TextComponentCodec())

    def serialize(self, *, field: MapIconStruct) -> bytes:
        return b"".join(
            [
                self.varint.serialize(field=field.type_),
                self.byte.serialize(field=field.x),
                self.byte.serialize(field=field.z),
                self.byte.serialize(field=field.direction),
                self.opt_text.serialize(field=field.display_name),
            ]
        )

    def deserialize(self, data: bytes) -> Deserialized[MapIconStruct]:
        t, c1 = self.varint.deserialize(data)
        x, c2 = self.byte.deserialize(data[c1:])
        z, c3 = self.byte.deserialize(data[c1 + c2 :])
        d, c4 = self.byte.deserialize(data[c1 + c2 + c3 :])
        name, c5 = self.opt_text.deserialize(data[c1 + c2 + c3 + c4 :])
        return MapIconStruct(t, x, z, d, name), c1 + c2 + c3 + c4 + c5


class MapColorPatchStruct(Struct):
    """Map color patch struct."""

    columns: int
    rows: int | None = None
    x: int | None = None
    z: int | None = None
    data: list[int] | None = None


class MapColorPatchCodec(Codec[MapColorPatchStruct]):
    """Map color patch codec."""

    def __init__(self) -> None:
        self.ubyte = UnsignedByteCodec()
        self.array: ArrayCodec = ArrayCodec(self.ubyte)

    def serialize(self, *, field: MapColorPatchStruct) -> bytes:
        out = bytearray(self.ubyte.serialize(field=field.columns))
        if field.columns > 0:
            if (
                field.rows is None
                or field.x is None
                or field.z is None
                or field.data is None
            ):
                raise EncodeError(
                    info="Rows, X, Z and Data must be present if columns > 0"
                )
            out.extend(self.ubyte.serialize(field=field.rows))
            out.extend(self.ubyte.serialize(field=field.x))
            out.extend(self.ubyte.serialize(field=field.z))
            out.extend(self.array.serialize(field=field.data))
        return bytes(out)

    def deserialize(self, data: bytes) -> Deserialized[MapColorPatchStruct]:
        columns, consumed = self.ubyte.deserialize(data)
        if columns > 0:
            rows, c1 = self.ubyte.deserialize(data[consumed:])
            x, c2 = self.ubyte.deserialize(data[consumed + c1 :])
            z, c3 = self.ubyte.deserialize(data[consumed + c1 + c2 :])
            arr, c4 = self.array.deserialize(data[consumed + c1 + c2 + c3 :])
            consumed += c1 + c2 + c3 + c4
            return MapColorPatchStruct(columns, rows, x, z, arr), consumed
        return MapColorPatchStruct(columns), consumed
