from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import (
    Boolean,
    Byte,
    Identifier,
    Long,
    Position,
    UByte,
    VarInt,
)


class Respawn(Packet, kw_only=True):
    """Packet representing Respawn (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x50

    dimension_type: VarInt
    """
    VarInt - The ID of type of dimension in
    theminecraft:dimension_typeregistry, defined by theRegistry Datapacket.
    """

    dimension_name: Identifier
    """Identifier - Name of the dimension being spawned into."""

    hashed_seed: Long
    """
    Long - First 8 bytes of the SHA-256 hash of the world's seed. Used
    client-side for biome noise
    """

    game_mode: UByte
    """Unsigned Byte - 0: Survival, 1: Creative, 2: Adventure, 3: Spectator."""

    previous_game_mode: Byte
    """
    Byte - -1: Undefined (null), 0: Survival, 1: Creative, 2: Adventure, 3:
    Spectator. The previous game mode. Vanilla client uses this for the
    debug (F3 + N & F3 + F4) game mode switch. (More information needed)
    """

    is_debug: Boolean
    """
    Boolean - True if the world is adebug modeworld; debug mode worlds
    cannot be modified and have predefined blocks.
    """

    is_flat: Boolean
    """
    Boolean - True if the world is asuperflatworld; flat worlds have
    different void fog and a horizon at y=0 instead of y=63.
    """

    has_death_location: Boolean
    """Boolean - If true, then the next two fields are present."""

    death_dimension_name: Identifier | None = None
    """OptionalIdentifier - Name of the dimension the player died in."""

    death_location: Position | None = None
    """OptionalPosition - The location that the player died at."""

    portal_cooldown: VarInt
    """
    VarInt - The number of ticks until the player can use the portal again.
    """

    sea_level: VarInt
    """VarInt"""

    data_kept: Byte
    """
    Byte - Bit mask. 0x01: Keep attributes, 0x02: Keep metadata. Tells
    which data should be kept on the client side once the player has
    respawned.In the vanilla implementation, this is context-
    dependent:normal respawns (after death) keep no data;exiting the end
    poem/credits keeps the attributes;other dimension changes (portals or
    teleports) keep all data.
    """
