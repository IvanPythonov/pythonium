from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Byte, Double, VarInt


class SetPlayerPosition(Packet, kw_only=True):
    """Packet representing SetPlayerPosition (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x1D

    x: Double
    """Double - Absolute position."""

    feet_y: Double
    """Double - Absolute feet position, normally Head Y - 1.62."""

    z: Double
    """Double - Absolute position."""

    flags: Byte
    """Byte - Bit field: 0x01: on ground, 0x02: pushing against wall."""
