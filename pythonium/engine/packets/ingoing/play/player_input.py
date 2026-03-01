from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import UByte, VarInt


class PlayerInput(Packet, kw_only=True):
    """Packet representing PlayerInput (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x2A

    flags: UByte
    """Unsigned Byte - Bit mask; see below"""
