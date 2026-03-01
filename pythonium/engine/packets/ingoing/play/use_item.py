from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Float, VarInt


class UseItem(Packet, kw_only=True):
    """Packet representing UseItem (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x40

    hand: VarInt
    """VarIntEnum - Hand used for the animation. 0: main hand, 1: off hand."""

    sequence: VarInt
    """VarInt - Block change sequence number (see#Acknowledge Block Change)."""

    yaw: Float
    """Float - Player head rotation around the Y-Axis."""

    pitch: Float
    """Float - Player head rotation around the X-Axis."""
