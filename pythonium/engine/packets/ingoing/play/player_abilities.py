from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Byte, VarInt


class PlayerAbilities(Packet, kw_only=True):
    """Packet representing PlayerAbilities (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x27

    flags: Byte
    """Byte - Bit mask. 0x02: is flying."""
