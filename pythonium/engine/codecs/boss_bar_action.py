from msgspec import Struct

from pythonium.engine.codecs import resolve_codec
from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import VarIntCodec
from pythonium.engine.exceptions import ActionError
from pythonium.engine.typealiases import Deserialized


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

        self.codecs = {
            0: resolve_codec(AddAction),
            1: resolve_codec(RemoveAction),
            2: resolve_codec(UpdateHealthAction),
            3: resolve_codec(UpdateTitleAction),
            4: resolve_codec(UpdateStyleAction),
            5: resolve_codec(UpdateFlagsAction),
        }

    def serialize(self, *, field: BossBarAction) -> bytes:
        action_map = {
            AddAction: 0,
            RemoveAction: 1,
            UpdateHealthAction: 2,
            UpdateTitleAction: 3,
            UpdateStyleAction: 4,
            UpdateFlagsAction: 5,
        }
        action_id = action_map[type(field)]

        return self.varint.serialize(field=action_id) + self.codecs[
            action_id
        ].serialize(field=field)

    def deserialize(self, data: bytes) -> Deserialized[BossBarAction]:
        action_id, consumed = self.varint.deserialize(data)

        if action_id not in self.codecs:
            raise ActionError(info=f"Unknown BossBar action ID: {action_id}")

        action_data, action_consumed = self.codecs[action_id].deserialize(
            data[consumed:]
        )
        return action_data, consumed + action_consumed
