from msgspec import Struct

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import VarIntCodec
from pythonium.engine.typealiases import Deserialized


class SlotStruct(Struct):
    """
    Structure representing an Item Slot in Minecraft 1.21.x.

    Currently supports basic items without complex Data Components.
    """

    item_count: int
    item_id: int | None = None


class SlotCodec(Codec[SlotStruct]):
    """Codec for the Slot type."""

    def __init__(self) -> None:
        self.varint_codec = VarIntCodec()

    def serialize(self, *, field: SlotStruct) -> bytes:
        if field.item_count <= 0 or field.item_id is None:
            return self.varint_codec.serialize(field=0)

        chunks = [
            self.varint_codec.serialize(field=field.item_count),
            self.varint_codec.serialize(field=field.item_id),
            self.varint_codec.serialize(field=0),
            self.varint_codec.serialize(field=0),
        ]

        return b"".join(chunks)

    def deserialize(self, data: bytes) -> Deserialized[SlotStruct]:
        count, offset = self.varint_codec.deserialize(data)

        if count <= 0:
            return SlotStruct(item_count=0, item_id=None), offset

        item_id, consumed = self.varint_codec.deserialize(data[offset:])
        offset += consumed

        added_components_count, consumed = self.varint_codec.deserialize(
            data[offset:]
        )
        offset += consumed

        if added_components_count > 0:
            msg = f"Cannot parse slot with {added_components_count}"

            raise NotImplementedError(msg)

        removed_components_count, consumed = self.varint_codec.deserialize(
            data[offset:]
        )
        offset += consumed

        for _ in range(removed_components_count):
            _, consumed = self.varint_codec.deserialize(data[offset:])
            offset += consumed

        return SlotStruct(item_count=count, item_id=item_id), offset
