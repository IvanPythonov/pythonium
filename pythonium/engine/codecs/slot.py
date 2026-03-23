from msgspec import Struct

from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import VarIntCodec
from pythonium.engine.codecs.optional import OptionalCodec
from pythonium.engine.codecs.primitives import (
    BooleanCodec,
    IntCodec,
    ShortCodec,
)
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


class AddedComponentStruct(Struct):
    """Added component struct."""

    component_type: int  # VarInt Enum
    component_data_hash: int  # Int (CRC32C)


class AddedComponentCodec(Codec[AddedComponentStruct]):
    """Added component codec."""

    def __init__(self) -> None:
        self.varint = VarIntCodec()
        self.int_codec = IntCodec()

    def serialize(self, *, field: AddedComponentStruct) -> bytes:
        return self.varint.serialize(
            field=field.component_type
        ) + self.int_codec.serialize(field=field.component_data_hash)

    def deserialize(self, data: bytes) -> Deserialized[AddedComponentStruct]:
        comp_type, c1 = self.varint.deserialize(data)
        comp_hash, c2 = self.int_codec.deserialize(data[c1:])
        return AddedComponentStruct(comp_type, comp_hash), c1 + c2


class HashedSlotStruct(Struct):
    """Hashed slot struct."""

    has_item: bool
    item_id: int | None = None
    item_count: int | None = None
    components_to_add: list[AddedComponentStruct] | None = None
    components_to_remove: list[int] | None = None


class HashedSlotCodec(Codec[HashedSlotStruct]):
    """Hashed slot codec."""

    def __init__(self) -> None:
        self.boolean = BooleanCodec()
        self.opt_varint = OptionalCodec(VarIntCodec())
        self.opt_add_array: OptionalCodec = OptionalCodec(
            ArrayCodec(AddedComponentCodec())
        )
        self.opt_rem_array: OptionalCodec = OptionalCodec(
            ArrayCodec(VarIntCodec())
        )

    def serialize(self, *, field: HashedSlotStruct) -> bytes:
        out = bytearray(self.boolean.serialize(field=field.has_item))

        if field.has_item:
            out.extend(self.opt_varint.serialize(field=field.item_id))
            out.extend(self.opt_varint.serialize(field=field.item_count))
            out.extend(
                self.opt_add_array.serialize(field=field.components_to_add)
            )
            out.extend(
                self.opt_rem_array.serialize(field=field.components_to_remove)
            )

        return bytes(out)

    def deserialize(self, data: bytes) -> Deserialized[HashedSlotStruct]:
        has_item, offset = self.boolean.deserialize(data)

        if not has_item:
            return HashedSlotStruct(has_item=False), offset

        item_id, c = self.opt_varint.deserialize(data[offset:])
        offset += c

        item_count, c = self.opt_varint.deserialize(data[offset:])
        offset += c

        comp_add, c = self.opt_add_array.deserialize(data[offset:])
        offset += c

        comp_rem, c = self.opt_rem_array.deserialize(data[offset:])
        offset += c

        return HashedSlotStruct(
            has_item=True,
            item_id=item_id,
            item_count=item_count,
            components_to_add=comp_add,
            components_to_remove=comp_rem,
        ), offset


class ChangedSlotStruct(Struct):
    """Changed Slot struct."""

    slot_number: int  # Short
    slot_data: HashedSlotStruct


class ChangedSlotCodec(Codec[ChangedSlotStruct]):
    """Changed slot codec."""

    def __init__(self) -> None:
        self.short = ShortCodec()
        self.hashed_slot = HashedSlotCodec()

    def serialize(self, *, field: ChangedSlotStruct) -> bytes:
        return self.short.serialize(
            field=field.slot_number
        ) + self.hashed_slot.serialize(field=field.slot_data)

    def deserialize(self, data: bytes) -> Deserialized[ChangedSlotStruct]:
        slot_num, c1 = self.short.deserialize(data)
        slot_data, c2 = self.hashed_slot.deserialize(data[c1:])
        return ChangedSlotStruct(slot_num, slot_data), c1 + c2
