from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class PlayerCommand(Packet, kw_only=True):
    """Packet representing PlayerCommand (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x29

    entity_id: VarInt
    """VarInt - Player ID (ignored by the vanilla server)"""

    action_id: VarInt
    """VarIntEnum - The ID of the action, see below."""

    jump_boost: VarInt
    """
    VarInt - Only used by the “start jump with horse” action, in which case
    it ranges from 0 to 100. In all other cases it is 0.
    """
