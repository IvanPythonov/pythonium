from msgspec import Struct

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import VarIntCodec
from pythonium.engine.typealiases import Deserialized


class StatisticStruct(Struct):
    """Statistic struct."""

    category_id: int
    statistic_id: int
    value: int


class StatisticCodec(Codec[StatisticStruct]):
    """Statistic codec."""

    def __init__(self) -> None:
        self.varint = VarIntCodec()

    def serialize(self, *, field: StatisticStruct) -> bytes:
        return b"".join(
            [
                self.varint.serialize(field=field.category_id),
                self.varint.serialize(field=field.statistic_id),
                self.varint.serialize(field=field.value),
            ]
        )

    def deserialize(self, data: bytes) -> Deserialized[StatisticStruct]:
        cat_id, c1 = self.varint.deserialize(data)
        stat_id, c2 = self.varint.deserialize(data[c1:])
        val, c3 = self.varint.deserialize(data[c1 + c2 :])
        return StatisticStruct(cat_id, stat_id, val), c1 + c2 + c3
