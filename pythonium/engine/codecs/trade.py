from msgspec import Struct

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.optional import OptionalCodec
from pythonium.engine.codecs.primitives import (
    BooleanCodec,
    FloatCodec,
    IntCodec,
)
from pythonium.engine.codecs.slot import SlotCodec, SlotStruct
from pythonium.engine.typealiases import Deserialized


class TradeStruct(Struct):
    """Struct representing trade."""

    input_item_1: SlotStruct
    output_item: SlotStruct
    input_item_2: SlotStruct | None
    disabled: bool
    uses: int
    max_uses: int
    xp: int
    special_price: int
    price_multiplier: float
    demand: int


class TradeCodec(Codec[TradeStruct]):
    """Trade codec."""

    def __init__(self) -> None:
        self.slot = SlotCodec()
        self.opt_slot = OptionalCodec(self.slot)
        self.boolean = BooleanCodec()
        self.int = IntCodec()
        self.float = FloatCodec()

    def serialize(self, *, field: TradeStruct) -> bytes:
        return b"".join(
            [
                self.slot.serialize(field=field.input_item_1),
                self.slot.serialize(field=field.output_item),
                self.opt_slot.serialize(field=field.input_item_2),
                self.boolean.serialize(field=field.disabled),
                self.int.serialize(field=field.uses),
                self.int.serialize(field=field.max_uses),
                self.int.serialize(field=field.xp),
                self.int.serialize(field=field.special_price),
                self.float.serialize(field=field.price_multiplier),
                self.int.serialize(field=field.demand),
            ]
        )

    def deserialize(self, data: bytes) -> Deserialized[TradeStruct]:
        in1, c1 = self.slot.deserialize(data)
        out, c2 = self.slot.deserialize(data[c1:])
        in2, c3 = self.opt_slot.deserialize(data[c1 + c2 :])
        disabled, c4 = self.boolean.deserialize(data[c1 + c2 + c3 :])
        uses, c5 = self.int.deserialize(data[c1 + c2 + c3 + c4 :])
        max_uses, c6 = self.int.deserialize(data[c1 + c2 + c3 + c4 + c5 :])
        xp, c7 = self.int.deserialize(data[c1 + c2 + c3 + c4 + c5 + c6 :])
        special, c8 = self.int.deserialize(
            data[c1 + c2 + c3 + c4 + c5 + c6 + c7 :]
        )
        mult, c9 = self.float.deserialize(
            data[c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 :]
        )
        demand, c10 = self.int.deserialize(
            data[c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 :]
        )

        return TradeStruct(
            input_item_1=in1,
            output_item=out,
            input_item_2=in2,
            disabled=disabled,
            uses=uses,
            max_uses=max_uses,
            xp=xp,
            special_price=special,
            price_multiplier=mult,
            demand=demand,
        ), c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 + c10
