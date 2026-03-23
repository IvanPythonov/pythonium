from msgspec import Struct

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.primitives import (
    ByteCodec,
    DoubleCodec,
    FloatCodec,
)
from pythonium.engine.typealiases import Deserialized


class MinecartStepStruct(Struct):
    """Struct representing minecraft step."""

    x: float
    y: float
    z: float
    velocity_x: float
    velocity_y: float
    velocity_z: float
    yaw: int
    pitch: int
    weight: float


class MinecartStepCodec(Codec[MinecartStepStruct]):
    """Minecraft step codec."""

    def __init__(self) -> None:
        self.double = DoubleCodec()
        self.byte = ByteCodec()
        self.float = FloatCodec()

    def serialize(self, *, field: MinecartStepStruct) -> bytes:
        return b"".join(
            [
                self.double.serialize(field=field.x),
                self.double.serialize(field=field.y),
                self.double.serialize(field=field.z),
                self.double.serialize(field=field.velocity_x),
                self.double.serialize(field=field.velocity_y),
                self.double.serialize(field=field.velocity_z),
                self.byte.serialize(field=field.yaw),
                self.byte.serialize(field=field.pitch),
                self.float.serialize(field=field.weight),
            ]
        )

    def deserialize(self, data: bytes) -> Deserialized[MinecartStepStruct]:
        x, c1 = self.double.deserialize(data)
        y, c2 = self.double.deserialize(data[c1:])
        z, c3 = self.double.deserialize(data[c1 + c2 :])
        vx, c4 = self.double.deserialize(data[c1 + c2 + c3 :])
        vy, c5 = self.double.deserialize(data[c1 + c2 + c3 + c4 :])
        vz, c6 = self.double.deserialize(data[c1 + c2 + c3 + c4 + c5 :])
        yaw, c7 = self.byte.deserialize(data[c1 + c2 + c3 + c4 + c5 + c6 :])
        pitch, c8 = self.byte.deserialize(
            data[c1 + c2 + c3 + c4 + c5 + c6 + c7 :]
        )
        weight, c9 = self.float.deserialize(
            data[c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 :]
        )

        return MinecartStepStruct(
            x, y, z, vx, vy, vz, yaw, pitch, weight
        ), c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9
