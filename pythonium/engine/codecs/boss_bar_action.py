from msgspec import Struct

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import TextComponentCodec, VarIntCodec
from pythonium.engine.codecs.primitives import FloatCodec, UnsignedByteCodec
from pythonium.engine.exceptions import ActionError
from pythonium.engine.typealiases import Deserialized

ADD_ACTION = 0
REMOVE_ACTION = 1
UPDATE_HEALTH_ACTION = 2
UPDATE_TITLE_ACTION = 3
UPDATE_STYLE_ACTION = 4
UPDATE_FLAGS_ACTION = 5


class BossBarAction(Struct):
    """Boss bar action."""


class AddAction(BossBarAction):
    """Add action."""

    title: dict
    health: float
    color: int
    dividers: int
    flags: int


class RemoveAction(BossBarAction):
    """Remove action."""


class UpdateHealthAction(BossBarAction):
    """Update health action."""

    health: float


class UpdateTitleAction(BossBarAction):
    """Update title action."""

    title: dict


class UpdateStyleAction(BossBarAction):
    """Update style action."""

    color: int
    dividers: int


class UpdateFlagsAction(BossBarAction):
    """Update flags action."""

    flags: int


class BossBarActionCodec(Codec[BossBarAction]):
    """Boss bar action codec."""

    def __init__(self) -> None:
        self.varint = VarIntCodec()
        self.text = TextComponentCodec()
        self.float = FloatCodec()
        self.ubyte = UnsignedByteCodec()

    def serialize(self, *, field: BossBarAction) -> bytes:
        if isinstance(field, AddAction):
            return b"".join(
                [
                    self.varint.serialize(field=ADD_ACTION),
                    self.text.serialize(field=field.title),
                    self.float.serialize(field=field.health),
                    self.varint.serialize(field=field.color),
                    self.varint.serialize(field=field.dividers),
                    self.ubyte.serialize(field=field.flags),
                ]
            )
        if isinstance(field, RemoveAction):
            return self.varint.serialize(field=REMOVE_ACTION)
        if isinstance(field, UpdateHealthAction):
            return self.varint.serialize(
                field=UPDATE_HEALTH_ACTION
            ) + self.float.serialize(field=field.health)
        if isinstance(field, UpdateTitleAction):
            return self.varint.serialize(
                field=UPDATE_TITLE_ACTION
            ) + self.text.serialize(field=field.title)
        if isinstance(field, UpdateStyleAction):
            return b"".join(
                [
                    self.varint.serialize(field=UPDATE_STYLE_ACTION),
                    self.varint.serialize(field=field.color),
                    self.varint.serialize(field=field.dividers),
                ]
            )
        if isinstance(field, UpdateFlagsAction):
            return self.varint.serialize(
                field=UPDATE_FLAGS_ACTION
            ) + self.ubyte.serialize(field=field.flags)
        raise ActionError(info="Unknown BossBarAction type")

    def deserialize(self, data: bytes) -> Deserialized[BossBarAction]:
        action_id, offset = self.varint.deserialize(data)

        if action_id == ADD_ACTION:
            title, c = self.text.deserialize(data[offset:])
            offset += c
            health, c = self.float.deserialize(data[offset:])
            offset += c
            color, c = self.varint.deserialize(data[offset:])
            offset += c
            dividers, c = self.varint.deserialize(data[offset:])
            offset += c
            flags, c = self.ubyte.deserialize(data[offset:])
            offset += c
            return AddAction(title, health, color, dividers, flags), offset

        if action_id == REMOVE_ACTION:
            return RemoveAction(), offset

        if action_id == UPDATE_HEALTH_ACTION:
            health, c = self.float.deserialize(data[offset:])
            offset += c
            return UpdateHealthAction(health), offset

        if action_id == UPDATE_TITLE_ACTION:
            title, c = self.text.deserialize(data[offset:])
            offset += c
            return UpdateTitleAction(title), offset

        if action_id == UPDATE_STYLE_ACTION:
            color, c = self.varint.deserialize(data[offset:])
            offset += c
            dividers, c = self.varint.deserialize(data[offset:])
            offset += c
            return UpdateStyleAction(color, dividers), offset

        if action_id == UPDATE_FLAGS_ACTION:
            flags, c = self.ubyte.deserialize(data[offset:])
            offset += c
            return UpdateFlagsAction(flags), offset

        raise ActionError(info=f"Unknown BossBar action ID: {action_id}")
