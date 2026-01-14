from typing import ClassVar

from msgspec import Struct
from msgspec.structs import fields as class_fields

from pythonium.engine.codecs import VarIntCodec, resolve_codec
from pythonium.engine.enums import Direction, State
from pythonium.engine.field import Field
from pythonium.engine.packets.packet_storage import PacketStorage
from pythonium.engine.types import VarInt


class Packet(Struct, kw_only=True):
    """Base packet."""

    __state__: ClassVar[State]
    __direction__: ClassVar[Direction]

    packet_id: ClassVar[VarInt]

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        required_fields = (
            "packet_id",
            "__state__",
            "__direction__",
        )

        for field in required_fields:
            if not hasattr(cls, field):
                msg = (
                    f"{cls.__name__} used Packet, but doesn't have `{field}`."
                )
                raise NotImplementedError(msg)

        PacketStorage.add(packet=cls)

    @classmethod
    def fields(cls) -> list[Field]:
        return build_schema(cls)


def build_schema(cls: type[Packet]) -> list[Field]:
    schema_fields: list[Field] = []

    for field in class_fields(cls):
        if field.name.startswith("__"):
            continue

        codec = resolve_codec(field.type.__value__)
        schema_fields.append(
            Field(
                name=field.name,
                codec=codec,
            )
        )
    return schema_fields


def serialize(packet: Packet) -> bytes:
    payload = bytearray()
    for field in packet.fields():
        payload.extend(field.serialize(getattr(packet, field.name)))

    data_to_be_sent = VarIntCodec().serialize(packet.packet_id) + payload

    return (
        VarIntCodec().serialize(len(data_to_be_sent)) + data_to_be_sent
    )  # HOORAY I FIXED THIS SHIT


def deserialize(cls: type[Packet], data: bytes) -> Packet:
    offset = 0

    kwargs = {}

    for field in cls.fields():
        value, consumed = field.deserialize(data[offset:])

        kwargs[field.name] = value
        offset += consumed

    return cls(**kwargs)
