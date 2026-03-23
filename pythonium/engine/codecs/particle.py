from msgspec import Struct

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import VarIntCodec
from pythonium.engine.codecs.primitives import FloatCodec
from pythonium.engine.typealiases import Deserialized


class ParticleDataStruct(Struct):
    """Particle data struct."""

    particle_id: int
    data: bytes  # ebaniy pizdec...


class ParticleDataCodec(Codec[ParticleDataStruct]):
    """Particle data codec."""

    def __init__(self) -> None:
        self.varint = VarIntCodec()

    def serialize(self, *, field: ParticleDataStruct) -> bytes:
        return self.varint.serialize(field=field.particle_id) + field.data

    def deserialize(self, data: bytes) -> Deserialized[ParticleDataStruct]:
        p_id, c = self.varint.deserialize(data)
        return ParticleDataStruct(p_id, b""), c


class BlockParticleAlternativeStruct(Struct):
    """Block particle alternative struct."""

    particle_data: ParticleDataStruct
    scaling: float
    speed: float
    weight: int


class BlockParticleAlternativeCodec(Codec[BlockParticleAlternativeStruct]):
    """Block particle altirnative codec."""

    def __init__(self) -> None:
        self.particle = ParticleDataCodec()
        self.float = FloatCodec()
        self.varint = VarIntCodec()

    def serialize(self, *, field: BlockParticleAlternativeStruct) -> bytes:
        return b"".join(
            [
                self.particle.serialize(field=field.particle_data),
                self.float.serialize(field=field.scaling),
                self.float.serialize(field=field.speed),
                self.varint.serialize(field=field.weight),
            ]
        )

    def deserialize(
        self, data: bytes
    ) -> Deserialized[BlockParticleAlternativeStruct]:
        p_data, c1 = self.particle.deserialize(data)
        scale, c2 = self.float.deserialize(data[c1:])
        speed, c3 = self.float.deserialize(data[c1 + c2 :])
        weight, c4 = self.varint.deserialize(data[c1 + c2 + c3 :])
        return BlockParticleAlternativeStruct(
            p_data, scale, speed, weight
        ), c1 + c2 + c3 + c4
