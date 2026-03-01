from typing import Annotated, Any, ClassVar

from msgspec import Struct

from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import (
    PositionCodec,
    StringCodec,
    VarIntCodec,
)
from pythonium.engine.codecs.optional import OptionalCodec
from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.typealiases import Deserialized
from pythonium.engine.types import VarInt


class DebugPayload(Struct):
    """Debug Payload Container."""

    subscription_type: int
    data: Any


class DebugPayloadCodec(Codec[DebugPayload]):
    """Debug payload codec."""

    def __init__(self) -> None:
        self.varint_codec = VarIntCodec()
        self.pos_codec = PositionCodec()
        self.opt_pos_codec = OptionalCodec(PositionCodec())
        self.string_codec = StringCodec()

    def serialize(self, *, field: DebugPayload) -> bytes:
        return self.varint_codec.serialize(field=field.subscription_type)

    def deserialize(self, data: bytes) -> Deserialized[DebugPayload]:
        sub_type, offset = self.varint_codec.deserialize(data)

        payload_value: Any = None
        consumed = 0

        remaining_data = data[offset:]

        match sub_type:
            case 0:
                payload_value = None
                consumed = 0

            case 1:
                hive, c1 = self.opt_pos_codec.deserialize(remaining_data)
                flower, c2 = self.opt_pos_codec.deserialize(
                    remaining_data[c1:]
                )
                travel, c3 = self.varint_codec.deserialize(
                    remaining_data[c1 + c2 :]
                )
                blacklist, c4 = ArrayCodec(self.pos_codec).deserialize(  # type: ignore[var-annotated]
                    remaining_data[c1 + c2 + c3 :]
                )

                payload_value = {
                    "hive_pos": hive,
                    "flower_pos": flower,
                    "travel_ticks": travel,
                    "blacklisted_hives": blacklist,
                }
                consumed = c1 + c2 + c3 + c4

            case 3:
                target, c1 = OptionalCodec(self.varint_codec).deserialize(
                    remaining_data
                )
                jump, c2 = self.opt_pos_codec.deserialize(remaining_data[c1:])

                payload_value = {"attack_target": target, "jump_target": jump}
                consumed = c1 + c2

            case _:
                payload_value = None
                consumed = 0

        return DebugPayload(
            subscription_type=sub_type, data=payload_value
        ), offset + consumed


type DebugType = Annotated[DebugPayload, DebugPayloadCodec()]


class DebugEvent(Packet, kw_only=True):
    """Packet representing a debug subscription event."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x1F

    payload: DebugType

    @property
    def subscription_type(self) -> int:
        return self.payload.subscription_type

    @property
    def data(self) -> Any:  # noqa: ANN401
        return self.payload.data
