from typing import (
    ClassVar,
)

from msgspec import Struct
from msgspec.structs import fields as class_fields

from pythonium.engine.codecs import VarIntCodec, resolve_codec
from pythonium.engine.enums import Direction, State
from pythonium.engine.field import Field
from pythonium.engine.packets import PacketStorage
from pythonium.engine.types import VarInt


class Packet(Struct):
    """Base packet."""

    fields: ClassVar[list[Field]]

    __state__: State
    __direction__: Direction

    packet_id: VarInt

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.fields = build_schema(cls)

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


def build_schema(cls: type[Packet]) -> list[Field]:
    schema_fields: list[Field] = []
    for field in class_fields(cls):
        if field.name.startswith("__"):
            continue
        codec = resolve_codec(field.type)
        schema_fields.append(
            Field(
                name=field.name,
                codec=codec,
            )
        )
    return schema_fields


def serialize(packet: Packet) -> bytes:
    out = bytearray()

    for field in packet.fields:
        out.extend(field.serialize(value=getattr(packet, field.name)))

    return VarIntCodec().serialize(field=len(out)) + out


def deserialize(cls: type[Packet], data: bytes) -> Packet:
    offset = 0

    _length, consumed = VarIntCodec().deserialize(data)
    offset += consumed

    packet_id, consumed = VarIntCodec().deserialize(data[offset:])
    offset += consumed

    if packet_id != cls.packet_id:
        msg = "Packet ID mismatch (expected {cls.packet_id}, got {packet_id})"
        raise ValueError(msg)

    kwargs = {}

    for field in cls.fields:
        value, consumed = field.deserialize(data[offset:])
        kwargs[field.name] = value
        offset += consumed

    return cls(**kwargs)
