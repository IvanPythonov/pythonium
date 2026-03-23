from msgspec import Struct

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import (
    PositionCodec,
    StringCodec,
    VarIntCodec,
)
from pythonium.engine.codecs.primitives import (
    BooleanCodec,
    ByteCodec,
    LongCodec,
    UnsignedByteCodec,
)
from pythonium.engine.exceptions import EncodeError
from pythonium.engine.typealiases import Deserialized


class WorldStateStruct(Struct, kw_only=True):
    """World state struct."""

    dimension_type: int
    dimension_name: str
    hashed_seed: int
    game_mode: int
    previous_game_mode: int
    is_debug: bool
    is_flat: bool
    has_death_location: bool
    death_dimension_name: str | None = None
    death_location: tuple[int, int, int] | None = None
    portal_cooldown: int
    sea_level: int


class WorldStateCodec(Codec[WorldStateStruct]):
    """World state codec."""

    def __init__(self) -> None:
        self.varint = VarIntCodec()
        self.string = StringCodec()
        self.long = LongCodec()
        self.ubyte = UnsignedByteCodec()
        self.byte = ByteCodec()
        self.boolean = BooleanCodec()

        self.position = PositionCodec()

    def serialize(self, *, field: WorldStateStruct) -> bytes:
        out = bytearray()
        out.extend(self.varint.serialize(field=field.dimension_type))
        out.extend(self.string.serialize(field=field.dimension_name))
        out.extend(self.long.serialize(field=field.hashed_seed))
        out.extend(self.ubyte.serialize(field=field.game_mode))
        out.extend(self.byte.serialize(field=field.previous_game_mode))
        out.extend(self.boolean.serialize(field=field.is_debug))
        out.extend(self.boolean.serialize(field=field.is_flat))
        out.extend(self.boolean.serialize(field=field.has_death_location))

        if field.has_death_location:
            if (
                field.death_dimension_name is None
                or field.death_location is None
            ):
                raise EncodeError(
                    info=(
                        "death_dimension_name and death_location must be"
                        "present if has_death_location is True"
                    )
                )
            out.extend(self.string.serialize(field=field.death_dimension_name))
            out.extend(self.position.serialize(field=field.death_location))

        out.extend(self.varint.serialize(field=field.portal_cooldown))
        out.extend(self.varint.serialize(field=field.sea_level))

        return bytes(out)

    def deserialize(self, data: bytes) -> Deserialized[WorldStateStruct]:
        offset = 0

        dim_type, c = self.varint.deserialize(data[offset:])
        offset += c

        dim_name, c = self.string.deserialize(data[offset:])
        offset += c

        seed, c = self.long.deserialize(data[offset:])
        offset += c

        gm, c = self.ubyte.deserialize(data[offset:])
        offset += c

        prev_gm, c = self.byte.deserialize(data[offset:])
        offset += c

        is_debug, c = self.boolean.deserialize(data[offset:])
        offset += c

        is_flat, c = self.boolean.deserialize(data[offset:])
        offset += c

        has_death, c = self.boolean.deserialize(data[offset:])
        offset += c

        death_dim = None
        death_loc = None
        if has_death:
            death_dim, c = self.string.deserialize(data[offset:])
            offset += c
            death_loc, c = self.position.deserialize(data[offset:])
            offset += c

        portal, c = self.varint.deserialize(data[offset:])
        offset += c

        sea_level, c = self.varint.deserialize(data[offset:])
        offset += c

        return WorldStateStruct(
            dimension_type=dim_type,
            dimension_name=dim_name,
            hashed_seed=seed,
            game_mode=gm,
            previous_game_mode=prev_gm,
            is_debug=is_debug,
            is_flat=is_flat,
            has_death_location=has_death,
            death_dimension_name=death_dim,
            death_location=death_loc,
            portal_cooldown=portal,
            sea_level=sea_level,
        ), offset
