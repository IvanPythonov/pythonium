from msgspec import Struct

from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import (
    StringCodec,
    TextComponentCodec,
    VarIntCodec,
)
from pythonium.engine.codecs.primitives import ByteCodec
from pythonium.engine.typealiases import Deserialized


class TeamInfoStruct(Struct):
    """Team info struct."""

    display_name: dict
    friendly_flags: int
    name_tag_visibility: int
    collision_rule: int
    team_color: int
    prefix: dict
    suffix: dict


class UpdateTeamStruct(Struct):
    """Update team struct."""

    team_name: str
    method: int
    team_info: TeamInfoStruct | None = None
    entities: list[str] | None = None


class UpdateTeamCodec(Codec[UpdateTeamStruct]):
    """Codec for Teams."""

    def __init__(self) -> None:
        self.string: StringCodec = StringCodec()
        self.byte: ByteCodec = ByteCodec()
        self.text: TextComponentCodec = TextComponentCodec()
        self.varint: VarIntCodec = VarIntCodec()
        self.string_array: ArrayCodec = ArrayCodec(self.string)

    def _serialize_info(self, info: TeamInfoStruct) -> bytes:
        return b"".join(
            [
                self.text.serialize(field=info.display_name),
                self.byte.serialize(field=info.friendly_flags),
                self.varint.serialize(field=info.name_tag_visibility),
                self.varint.serialize(field=info.collision_rule),
                self.varint.serialize(field=info.team_color),
                self.text.serialize(field=info.prefix),
                self.text.serialize(field=info.suffix),
            ]
        )

    def serialize(self, *, field: UpdateTeamStruct) -> bytes:
        out = bytearray()
        out.extend(self.string.serialize(field=field.team_name))
        out.extend(self.byte.serialize(field=field.method))

        if field.method in (0, 2):
            out.extend(self._serialize_info(field.team_info))
        if field.method in (0, 3, 4):
            out.extend(self.string_array.serialize(field=field.entities or []))

        return bytes(out)

    def deserialize(self, data: bytes) -> Deserialized[UpdateTeamStruct]:
        name, c1 = self.string.deserialize(data)
        method, c2 = self.byte.deserialize(data[c1:])
        consumed = c1 + c2

        info, entities = None, None

        if method in (0, 2):
            dn, c3 = self.text.deserialize(data[consumed:])
            ff, c4 = self.byte.deserialize(data[consumed + c3 :])
            ntv, c5 = self.varint.deserialize(data[consumed + c3 + c4 :])
            cr, c6 = self.varint.deserialize(data[consumed + c3 + c4 + c5 :])
            tc, c7 = self.varint.deserialize(
                data[consumed + c3 + c4 + c5 + c6 :]
            )
            pfx, c8 = self.text.deserialize(
                data[consumed + c3 + c4 + c5 + c6 + c7 :]
            )
            sfx, c9 = self.text.deserialize(
                data[consumed + c3 + c4 + c5 + c6 + c7 + c8 :]
            )
            info = TeamInfoStruct(dn, ff, ntv, cr, tc, pfx, sfx)
            consumed += c3 + c4 + c5 + c6 + c7 + c8 + c9

        if method in (0, 3, 4):
            entities, c10 = self.string_array.deserialize(data[consumed:])
            consumed += c10

        return UpdateTeamStruct(name, method, info, entities), consumed
