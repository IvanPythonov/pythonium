from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class SwingArm(Packet, kw_only=True):
    """Packet representing SwingArm (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x3C

    hand: VarInt
    """VarIntEnum - Hand used for the animation. 0: main hand, 1: off hand."""
