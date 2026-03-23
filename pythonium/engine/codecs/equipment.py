from msgspec import Struct

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.primitives import ByteCodec
from pythonium.engine.codecs.slot import SlotCodec, SlotStruct
from pythonium.engine.typealiases import Deserialized


class EquipmentEntryStruct(Struct):
    """Equipment entry struct."""

    slot: int
    item: SlotStruct


class EquipmentArrayCodec(Codec[list[EquipmentEntryStruct]]):
    """Codec for Equipment Array."""

    def __init__(self) -> None:
        self.byte = ByteCodec()
        self.slot = SlotCodec()

    def serialize(self, *, field: list[EquipmentEntryStruct]) -> bytes:
        out = bytearray()
        for i, entry in enumerate(field):
            slot_id = entry.slot | 0x80 if i < len(field) - 1 else entry.slot
            out.extend(self.byte.serialize(field=slot_id))
            out.extend(self.slot.serialize(field=entry.item))
        return bytes(out)

    def deserialize(
        self, data: bytes
    ) -> Deserialized[list[EquipmentEntryStruct]]:
        entries = []
        offset = 0
        while True:
            slot_byte, c1 = self.byte.deserialize(data[offset:])
            item, c2 = self.slot.deserialize(data[offset + c1 :])
            offset += c1 + c2

            slot_id = slot_byte & 0x7F
            entries.append(EquipmentEntryStruct(slot_id, item))

            if not (slot_byte & 0x80):
                break

        return entries, offset
