from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Float, Position, VarInt


class UseItemOn(Packet, kw_only=True):
    """Packet representing UseItemOn (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x3F

    hand: VarInt
    """
    VarIntEnum - The hand from which the block is placed; 0: main hand, 1:
    off hand.
    """

    location: Position
    """Position - Block position."""

    face: VarInt
    """
    VarIntEnum - The face on which the block is placed (as documented
    atPlayer Action).
    """

    cursor_position_x: Float
    """
    Float - The position of the crosshair on the block, from 0 to 1
    increasing from west to east.
    """

    cursor_position_y: Float
    """
    Float - The position of the crosshair on the block, from 0 to 1
    increasing from bottom to top.
    """

    cursor_position_z: Float
    """
    Float - The position of the crosshair on the block, from 0 to 1
    increasing from north to south.
    """

    inside_block: Boolean
    """Boolean - True when the player's head is inside of a block."""

    world_border_hit: Boolean
    """
    Boolean - Seems to always be false, even when interacting with blocks
    around or outside the world border, or while the player is outside the
    border.
    """

    sequence: VarInt
    """VarInt - Block change sequence number (see#Acknowledge Block Change)."""
