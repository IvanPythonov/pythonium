from msgspec import Struct

from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import (
    StringCodec,
    TextComponentCodec,
    VarIntCodec,
)
from pythonium.engine.codecs.optional import OptionalCodec
from pythonium.engine.codecs.primitives import (
    BooleanCodec,
    FloatCodec,
    IntCodec,
    LongCodec,
)
from pythonium.engine.codecs.slot import SlotCodec, SlotStruct
from pythonium.engine.typealiases import Deserialized


class AdvancementDisplayStruct(Struct):
    """Advancement display struct."""

    title: dict
    description: dict
    icon: SlotStruct
    frame_type: int
    flags: int
    background_texture: str | None
    x: float
    y: float


class AdvancementDisplayCodec(Codec[AdvancementDisplayStruct]):
    """Advancement display codec."""

    def __init__(self) -> None:
        self.text = TextComponentCodec()
        self.slot = SlotCodec()
        self.varint = VarIntCodec()
        self.int_codec = IntCodec()
        self.string = StringCodec()
        self.float_codec = FloatCodec()

    def serialize(self, *, field: AdvancementDisplayStruct) -> bytes:
        out = bytearray()
        out.extend(self.text.serialize(field=field.title))
        out.extend(self.text.serialize(field=field.description))
        out.extend(self.slot.serialize(field=field.icon))
        out.extend(self.varint.serialize(field=field.frame_type))
        out.extend(self.int_codec.serialize(field=field.flags))

        if field.flags & 0x01 and field.background_texture:
            out.extend(self.string.serialize(field=field.background_texture))

        out.extend(self.float_codec.serialize(field=field.x))
        out.extend(self.float_codec.serialize(field=field.y))
        return bytes(out)

    def deserialize(
        self, data: bytes
    ) -> Deserialized[AdvancementDisplayStruct]:
        title, c1 = self.text.deserialize(data)
        desc, c2 = self.text.deserialize(data[c1:])
        icon, c3 = self.slot.deserialize(data[c1 + c2 :])
        frame, c4 = self.varint.deserialize(data[c1 + c2 + c3 :])
        flags, c5 = self.int_codec.deserialize(data[c1 + c2 + c3 + c4 :])

        consumed = c1 + c2 + c3 + c4 + c5
        bg_tex = None

        if flags & 0x01:
            bg_tex, c = self.string.deserialize(data[consumed:])
            consumed += c

        x, cx = self.float_codec.deserialize(data[consumed:])
        y, cy = self.float_codec.deserialize(data[consumed + cx :])
        consumed += cx + cy

        return AdvancementDisplayStruct(
            title, desc, icon, frame, flags, bg_tex, x, y
        ), consumed


class AdvancementStruct(Struct):
    """Advancement struct."""

    parent_id: str | None
    display_data: AdvancementDisplayStruct | None
    nested_requirements: list[list[str]]
    sends_telemetry: bool


class AdvancementCodec(Codec[AdvancementStruct]):
    """Advancement codec."""

    def __init__(self) -> None:
        self.opt_string = OptionalCodec(StringCodec())
        self.opt_display = OptionalCodec(AdvancementDisplayCodec())
        self.req_array: ArrayCodec = ArrayCodec(ArrayCodec(StringCodec()))
        self.boolean = BooleanCodec()

    def serialize(self, *, field: AdvancementStruct) -> bytes:
        return b"".join(
            [
                self.opt_string.serialize(field=field.parent_id),
                self.opt_display.serialize(field=field.display_data),
                self.req_array.serialize(field=field.nested_requirements),
                self.boolean.serialize(field=field.sends_telemetry),
            ]
        )

    def deserialize(self, data: bytes) -> Deserialized[AdvancementStruct]:
        parent, c1 = self.opt_string.deserialize(data)
        display, c2 = self.opt_display.deserialize(data[c1:])
        reqs, c3 = self.req_array.deserialize(data[c1 + c2 :])
        telemetry, c4 = self.boolean.deserialize(data[c1 + c2 + c3 :])
        return AdvancementStruct(
            parent, display, reqs, telemetry
        ), c1 + c2 + c3 + c4


class AdvancementMappingStruct(Struct):
    """Advancement mapping struct."""

    key: str
    value: AdvancementStruct


class AdvancementMappingCodec(Codec[AdvancementMappingStruct]):
    """Advancement mapping codec."""

    def __init__(self) -> None:
        self.string = StringCodec()
        self.adv = AdvancementCodec()

    def serialize(self, *, field: AdvancementMappingStruct) -> bytes:
        return self.string.serialize(field=field.key) + self.adv.serialize(
            field=field.value
        )

    def deserialize(
        self, data: bytes
    ) -> Deserialized[AdvancementMappingStruct]:
        k, c1 = self.string.deserialize(data)
        v, c2 = self.adv.deserialize(data[c1:])
        return AdvancementMappingStruct(k, v), c1 + c2


class ProgressMappingStruct(Struct):
    """Progress mapping struct."""

    key: str
    criteria: list[
        tuple[str, int | None]
    ]  # tuple of (Identifier, Optional Long)


class ProgressMappingCodec(Codec[ProgressMappingStruct]):
    """Progress mapping codec."""

    def __init__(self) -> None:
        self.string = StringCodec()
        self.opt_long = OptionalCodec(LongCodec())

    def serialize(self, *, field: ProgressMappingStruct) -> bytes:
        out = bytearray(self.string.serialize(field=field.key))
        out.extend(VarIntCodec().serialize(field=len(field.criteria)))
        for crit_id, date in field.criteria:
            out.extend(self.string.serialize(field=crit_id))
            out.extend(self.opt_long.serialize(field=date))
        return bytes(out)

    def deserialize(self, data: bytes) -> Deserialized[ProgressMappingStruct]:
        k, offset = self.string.deserialize(data)
        count, c = VarIntCodec().deserialize(data[offset:])
        offset += c

        criteria = []
        for _ in range(count):
            crit_id, c1 = self.string.deserialize(data[offset:])
            date, c2 = self.opt_long.deserialize(data[offset + c1 :])
            offset += c1 + c2
            criteria.append((crit_id, date))

        return ProgressMappingStruct(k, criteria), offset
