from msgspec import Struct

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import StringCodec, VarIntCodec
from pythonium.engine.codecs.primitives import BooleanCodec, FloatCodec
from pythonium.engine.exceptions import EncodeError
from pythonium.engine.typealiases import Deserialized


class SoundEventStruct(Struct):
    """Sound event struct."""

    registry_id: int
    sound_name: str | None = None
    has_fixed_range: bool = False
    fixed_range: float | None = None


class SoundEventCodec(Codec[SoundEventStruct]):
    """Codec for 'ID or Sound Event' polymorphic type."""

    def __init__(self) -> None:
        self.varint = VarIntCodec()
        self.string = StringCodec()
        self.boolean = BooleanCodec()
        self.float = FloatCodec()

    def serialize(self, *, field: SoundEventStruct) -> bytes:
        out = bytearray(self.varint.serialize(field=field.registry_id))

        if field.registry_id == 0:
            if not field.sound_name:
                raise EncodeError(
                    info="sound_name must be present if registry_id is 0"
                )
            out.extend(self.string.serialize(field=field.sound_name))
            out.extend(self.boolean.serialize(field=field.has_fixed_range))
            if field.has_fixed_range and field.fixed_range is not None:
                out.extend(self.float.serialize(field=field.fixed_range))

        return bytes(out)

    def deserialize(self, data: bytes) -> Deserialized[SoundEventStruct]:
        reg_id, consumed = self.varint.deserialize(data)

        sound_name = None
        has_fixed = False
        fixed_range = None

        if reg_id == 0:
            sound_name, c1 = self.string.deserialize(data[consumed:])
            has_fixed, c2 = self.boolean.deserialize(data[consumed + c1 :])
            consumed += c1 + c2

            if has_fixed:
                fixed_range, c3 = self.float.deserialize(data[consumed:])
                consumed += c3

        return SoundEventStruct(
            reg_id, sound_name, has_fixed, fixed_range
        ), consumed
