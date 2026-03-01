from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import (
    Byte,
    Float,
    Position,
    String,
    VarInt,
    VarLong,
)


class ProgramStructureBlock(Packet, kw_only=True):
    """Packet representing ProgramStructureBlock (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x39

    location: Position
    """Position - Block entity location."""

    action: VarInt
    """
    VarIntEnum - An additional action to perform beyond simply saving the
    given data; see below.
    """

    mode: VarInt
    """VarIntEnum - One of SAVE (0), LOAD (1), CORNER (2), DATA (3)."""

    name: String
    """String(32767)"""

    offset_x: Byte
    """Byte - Between -48 and 48."""

    offset_y: Byte
    """Byte - Between -48 and 48."""

    offset_z: Byte
    """Byte - Between -48 and 48."""

    size_x: Byte
    """Byte - Between 0 and 48."""

    size_y: Byte
    """Byte - Between 0 and 48."""

    size_z: Byte
    """Byte - Between 0 and 48."""

    mirror: VarInt
    """VarIntEnum - One of NONE (0), LEFT_RIGHT (1), FRONT_BACK (2)."""

    rotation: VarInt
    """
    VarIntEnum - One of NONE (0), CLOCKWISE_90 (1), CLOCKWISE_180 (2),
    COUNTERCLOCKWISE_90 (3).
    """

    metadata: String
    """String(128)"""

    integrity: Float
    """Float - Between 0 and 1."""

    seed: VarLong
    """VarLong"""

    flags: Byte
    """
    Byte - 0x01: Ignore entities; 0x02: Show air; 0x04: Show bounding box;
    0x08: Strict placement.
    """
