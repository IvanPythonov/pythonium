from msgspec import Struct

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import StringCodec, TextComponentCodec
from pythonium.engine.codecs.optional import OptionalCodec
from pythonium.engine.typealiases import Deserialized


class CommandMatchStruct(Struct):
    """Command match struct."""

    match: str
    tooltip: dict | None = None


class CommandMatchCodec(Codec[CommandMatchStruct]):
    """Command match codec."""

    def __init__(self) -> None:
        self.string = StringCodec()
        self.opt_text = OptionalCodec(TextComponentCodec())

    def serialize(self, *, field: CommandMatchStruct) -> bytes:
        return self.string.serialize(
            field=field.match
        ) + self.opt_text.serialize(field=field.tooltip)

    def deserialize(self, data: bytes) -> Deserialized[CommandMatchStruct]:
        match_str, c1 = self.string.deserialize(data)
        tooltip, c2 = self.opt_text.deserialize(data[c1:])
        return CommandMatchStruct(match=match_str, tooltip=tooltip), c1 + c2
