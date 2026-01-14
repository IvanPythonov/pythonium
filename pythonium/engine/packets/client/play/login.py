from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets import Packet
from pythonium.engine.types import (
    Boolean,
    Int,
    Long,
    Position,
    String,
    StringArray,
    UByte,
    VarInt,
)


class Login(Packet, kw_only=True):
    """Packet representing login."""

    __state__ = State.LOGIN
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x30

    entity_id: Int
    is_hardcore: Boolean
    dimension_names: StringArray
    max_players: VarInt
    view_distance: VarInt
    simulation_distance: VarInt
    reduced_debug_info: Boolean
    enable_respawn_screen: Boolean
    do_limited_crafting: Boolean
    dimension_type: VarInt
    dimension_name: String
    hashed_seed: Long
    game_mode: UByte
    previous_game_mode: Int
    is_debug: Boolean
    is_flat: Boolean
    has_death_location: Boolean
    death_dimension_name: String
    death_location: Position
    portal_cooldown: VarInt
    sea_level: VarInt
    enforces_secure_chat: Boolean
