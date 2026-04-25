import logging
import types
from collections.abc import Callable
from enum import Enum
from typing import Any, ClassVar, Self, TypeAliasType, get_args

from msgspec import Struct, convert
from msgspec.json import decode, encode
from msgspec.structs import fields as class_fields

from pythonium.engine.codecs import (
    Codec,
    OptionalCodec,
    StringCodec,
    VarIntCodec,
    resolve_codec,
)
from pythonium.engine.enums import Direction, State
from pythonium.engine.field import Field
from pythonium.engine.formatter import format_packet
from pythonium.engine.packets.factory import SerializeFactory
from pythonium.engine.packets.packet_storage import PacketStorage
from pythonium.engine.types import VarInt
from pythonium.registries.protocol_storage import get_data_by_packet_name

_VARINT_CODEC = VarIntCodec()
_STRING_CODEC = StringCodec()
_UNION_TYPE_ARGS_COUNT = 2

logger = logging.getLogger(name=__name__)


def bake_all_packets() -> None:
    for packet in Packet.__subclasses__():
        packet.serialize = SerializeFactory.get(fields=packet.get_schema())


class Packet(Struct, kw_only=True):
    """Base packet."""

    __packet_name__: ClassVar[str]

    __schema_as_json__: ClassVar[bool] = False
    __schema_cache__: ClassVar[list[Field] | None] = None

    serialize: ClassVar[Callable[[Self], bytes]]
    deserialize: ClassVar[Callable[[bytes], Self]]

    state: ClassVar[State]
    direction: ClassVar[Direction]

    packet_id: ClassVar[VarInt]

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if not hasattr(cls, "__packet_name__"):
            msg = f"{cls.__name__} must define `__packet_name__`"
            raise NotImplementedError(msg)

        state, direction, packet_id = get_data_by_packet_name(
            packet_name=cls.__packet_name__
        )

        cls.state = state
        cls.direction = direction
        cls.packet_id = packet_id

        PacketStorage.add(packet=cls)

    @classmethod
    def get_schema(cls) -> list[Field]:
        if cls.__schema_cache__ is None:
            cls.__schema_cache__ = _build_schema(cls)
        return cls.__schema_cache__

    def __str__(self) -> str:
        return format_packet(self)

    def __repr__(self) -> str:
        return format_packet(self)


def _build_schema(cls: type[Packet]) -> list[Field]:
    """Build schema from class fields."""
    if cls.__schema_as_json__:
        return []

    schema: list[Field] = []

    for field in class_fields(cls):
        if field.name.startswith("__") or field.name in (
            "serialize",
            "deserialize",
        ):
            continue

        codec = _resolve_field_codec(field.type)

        schema.append(Field(name=field.name, codec=codec))

    return schema


def _resolve_field_codec(
    field_type: TypeAliasType | types.UnionType | type[Enum],
) -> Codec[Any]:
    """Resolve codec for field, wrapping in OptionalCodec if needed."""
    if isinstance(field_type, types.UnionType):
        args = get_args(field_type)
        non_none_args = [arg for arg in args if arg is not type(None)]

        if len(non_none_args) == 1 and len(args) == _UNION_TYPE_ARGS_COUNT:
            inner_codec = resolve_codec(non_none_args[0])
            return OptionalCodec(inner_codec)
        msg = f"Unsupported union type: {field_type}"
        raise TypeError(msg)

    if isinstance(field_type, type) and issubclass(field_type, Enum):
        if hasattr(field_type, "__codec__"):
            return field_type.__codec__
        msg = f"{field_type.__name__} used Enum, but doesn't have `__codec__`."
        raise NotImplementedError(msg)

    return resolve_codec(field_type)


def serialize(packet: Packet) -> bytes:
    """Serialize packet to bytes."""
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(packet)

    chunks = []

    if packet.__schema_as_json__:
        json_bytes = encode(packet)

        chunks.append(_VARINT_CODEC.serialize(field=packet.packet_id))
        chunks.append(_VARINT_CODEC.serialize(field=len(json_bytes)))
        chunks.append(json_bytes)
    else:
        chunks.append(packet.serialize())

    payload = b"".join(chunks)
    length_bytes = _VARINT_CODEC.serialize(field=len(payload))

    return length_bytes + payload


def deserialize(cls: type[Packet], data: bytes) -> Packet:
    """Deserialize bytes to packet."""
    offset = 0
    kwargs: dict[str, Any] = {}

    if cls.__schema_as_json__:
        value, _consumed = _STRING_CODEC.deserialize(data[offset:])
        return decode(value, type=cls)

    for field in cls.get_schema():
        value, consumed = field.codec.deserialize(data[offset:])

        kwargs[field.name] = value
        offset += consumed

    packet = convert(kwargs, type=cls)

    if logger.isEnabledFor(logging.DEBUG) and cls.__name__ not in (
        "TickEnd",
        "Position",
        "Look",
        "Flying",
        "PositionLook",
    ):
        logger.debug(packet)
    return packet
