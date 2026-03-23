from msgspec import Struct

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import VarIntCodec
from pythonium.engine.codecs.primitives import FloatCodec, UnsignedByteCodec
from pythonium.engine.typealiases import Deserialized


class WaypointColorStruct(Struct):
    """Waypoint color struct."""

    red: int
    green: int
    blue: int


class WaypointColorCodec(Codec[WaypointColorStruct]):
    """Waypoint color codec."""

    def __init__(self) -> None:
        self.ubyte = UnsignedByteCodec()

    def serialize(self, *, field: WaypointColorStruct) -> bytes:
        return b"".join(
            [
                self.ubyte.serialize(field=field.red),
                self.ubyte.serialize(field=field.green),
                self.ubyte.serialize(field=field.blue),
            ]
        )

    def deserialize(self, data: bytes) -> Deserialized[WaypointColorStruct]:
        r, c1 = self.ubyte.deserialize(data)
        g, c2 = self.ubyte.deserialize(data[c1:])
        b, c3 = self.ubyte.deserialize(data[c1 + c2 :])
        return WaypointColorStruct(r, g, b), c1 + c2 + c3


class WaypointDataStruct(Struct):
    """Waypoint data struct."""

    type_: int
    x: int | None = None
    y: int | None = None
    z: int | None = None
    azimuth: float | None = None


class WaypointDataCodec(Codec[WaypointDataStruct]):
    """Waypoint data codec."""

    def __init__(self) -> None:
        self.varint = VarIntCodec()
        self.float_codec = FloatCodec()

    def serialize(self, *, field: WaypointDataStruct) -> bytes:
        out = bytearray(self.varint.serialize(field=field.type_))
        if field.type_ == 1 and field.x and field.y and field.z:
            out.extend(self.varint.serialize(field=field.x))
            out.extend(self.varint.serialize(field=field.y))
            out.extend(self.varint.serialize(field=field.z))
        elif field.type_ == 2 and field.x and field.z:
            out.extend(self.varint.serialize(field=field.x))
            out.extend(self.varint.serialize(field=field.z))
        elif field.type_ == 3 and field.azimuth:
            out.extend(self.float_codec.serialize(field=field.azimuth))
        return bytes(out)

    def deserialize(self, data: bytes) -> Deserialized[WaypointDataStruct]:
        t, consumed = self.varint.deserialize(data)
        x, y, z, az = None, None, None, None

        if t == 1:
            x, c1 = self.varint.deserialize(data[consumed:])
            y, c2 = self.varint.deserialize(data[consumed + c1 :])
            z, c3 = self.varint.deserialize(data[consumed + c1 + c2 :])
            consumed += c1 + c2 + c3
        elif t == 2:
            x, c1 = self.varint.deserialize(data[consumed:])
            z, c2 = self.varint.deserialize(data[consumed + c1 :])
            consumed += c1 + c2
        elif t == 3:
            az, c1 = self.float_codec.deserialize(data[consumed:])
            consumed += c1

        return WaypointDataStruct(t, x, y, z, az), consumed
