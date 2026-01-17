import types
from typing import Any, ClassVar, TypeAliasType, get_args

from msgspec import Struct
from msgspec.json import decode, encode
from msgspec.structs import fields as class_fields

from pythonium.engine.classproperty import ClassProperty
from pythonium.engine.codecs import (
    Codec,
    OptionalCodec,
    StringCodec,
    VarIntCodec,
    resolve_codec,
)
from pythonium.engine.enums import Direction, State
from pythonium.engine.field import Field
from pythonium.engine.packets.packet_storage import PacketStorage
from pythonium.engine.types import VarInt

_VARINT_CODEC = VarIntCodec()
_STRING_CODEC = StringCodec()
_UNION_TYPE_ARGS_COUNT = 2


class Packet(Struct, kw_only=True):
    """Base packet."""

    __schema_as_json__: ClassVar[bool] = False
    __schema_cache__: ClassVar[list[Field] | None] = None

    __state__: ClassVar[State]
    __direction__: ClassVar[Direction]

    packet_id: ClassVar[VarInt]

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        required_attrs = ("packet_id", "__state__", "__direction__")

        for attr in required_attrs:
            if not hasattr(cls, attr):
                msg = f"{cls.__name__} must define `{attr}`"
                raise NotImplementedError(msg)

        PacketStorage.add(packet=cls)

    @ClassProperty[list[Field]]  # type: ignore[arg-type]
    def __schema__(cls) -> list[Field]:  # noqa: N805
        if cls.__schema_cache__ is None:
            cls.__schema_cache__ = _build_schema(cls)  # type: ignore[misc, arg-type]
        return cls.__schema_cache__


def _build_schema(cls: type[Packet]) -> list[Field]:
    """Build schema from class fields."""
    if cls.__schema_as_json__:
        return []

    schema: list[Field] = []

    for field in class_fields(cls):
        if field.name.startswith("__"):
            continue

        codec = _resolve_field_codec(field.type)
        schema.append(Field(name=field.name, codec=codec))

    return schema


def _resolve_field_codec(
    field_type: TypeAliasType | types.UnionType,
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
    return resolve_codec(field_type)


def serialize(packet: Packet) -> bytes:
    """Serialize packet to bytes."""
    payload = bytearray()

    if packet.__schema_as_json__:
        payload.extend(
            _STRING_CODEC.serialize(field=encode(packet).decode("utf-8"))
        )
    else:
        for field in packet.__schema__:
            value = getattr(packet, field.name)
            payload.extend(field.codec.serialize(field=value))

    packet_id_bytes = _VARINT_CODEC.serialize(field=packet.packet_id)
    packet_data = packet_id_bytes + payload

    length_bytes = _VARINT_CODEC.serialize(field=len(packet_data))

    return length_bytes + packet_data


def deserialize[P: Packet](cls: type[P], data: bytes) -> P:
    """Deserialize bytes to packet."""
    offset = 0
    kwargs: dict[str, Any] = {}

    if cls.__schema_as_json__:
        value, _consumed = _STRING_CODEC.deserialize(data[offset:])
        return decode(value, type=cls)

    for field in cls.__schema__:
        value, consumed = field.codec.deserialize(data[offset:])

        kwargs[field.name] = value
        offset += consumed

    return cls(**kwargs)
