from msgspec import Struct

from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import StringCodec, VarIntCodec
from pythonium.engine.typealiases import Deserialized


class TagStruct(Struct):
    """Tag struct."""

    tag_name: str
    entries: list[int]  # VarIntArray


class TagCodec(Codec[TagStruct]):
    """Tag codec."""

    def __init__(self) -> None:
        self.string = StringCodec()
        self.varint_array: ArrayCodec = ArrayCodec(VarIntCodec())

    def serialize(self, *, field: TagStruct) -> bytes:
        return self.string.serialize(
            field=field.tag_name
        ) + self.varint_array.serialize(field=field.entries)

    def deserialize(self, data: bytes) -> Deserialized[TagStruct]:
        name, c1 = self.string.deserialize(data)
        entries, c2 = self.varint_array.deserialize(data[c1:])
        return TagStruct(name, entries), c1 + c2


class RegistryTagsStruct(Struct):
    """Registry tags struct."""

    registry: str
    tags: list[TagStruct]


class RegistryTagsCodec(Codec[RegistryTagsStruct]):
    """Registry tags codec."""

    def __init__(self) -> None:
        self.string = StringCodec()
        self.tag_array: ArrayCodec = ArrayCodec(TagCodec())

    def serialize(self, *, field: RegistryTagsStruct) -> bytes:
        return self.string.serialize(
            field=field.registry
        ) + self.tag_array.serialize(field=field.tags)

    def deserialize(self, data: bytes) -> Deserialized[RegistryTagsStruct]:
        reg, c1 = self.string.deserialize(data)
        tags, c2 = self.tag_array.deserialize(data[c1:])
        return RegistryTagsStruct(reg, tags), c1 + c2
