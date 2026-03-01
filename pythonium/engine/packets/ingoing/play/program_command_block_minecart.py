from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, String, VarInt


class ProgramCommandBlockMinecart(Packet, kw_only=True):
    """Packet representing ProgramCommandBlockMinecart (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x36

    entity_id: VarInt
    """VarInt"""

    command: String
    """String(32767)"""

    track_output: Boolean
    """
    Boolean - If false, the output of the previous command will not be
    stored within the command block.
    """
