from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Identifier, Position, String, VarInt


class ProgramJigsawBlock(Packet, kw_only=True):
    """Packet representing ProgramJigsawBlock (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x38

    location: Position
    """Position - Block entity location"""

    name: Identifier
    """Identifier"""

    target: Identifier
    """Identifier"""

    pool: Identifier
    """Identifier"""

    final_state: String
    """String(32767) - "Turns into" on the GUI,final_statein NBT."""

    joint_type: String
    """
    String(32767) - rollableif the attached piece can be rotated,
    elsealigned.
    """

    selection_priority: VarInt
    """VarInt"""

    placement_priority: VarInt
    """VarInt"""
