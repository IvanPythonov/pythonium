from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Byte, Position, String, VarInt


class ProgramCommandBlock(Packet, kw_only=True):
    """Packet representing ProgramCommandBlock (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x35

    location: Position
    """Position"""

    command: String
    """String(32767)"""

    mode: VarInt
    """VarIntEnum - 0: chain, 1: repeating, 2: impulse."""

    flags: Byte
    """
    Byte - 0x01: Track Output (if false, the output of the previous command
    will not be stored within the command block); 0x02: Is conditional;
    0x04: Automatic.
    """
