from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Double, TextComponent, VarInt


class TestInstanceBlockStatus(Packet, kw_only=True):
    """Packet representing TestInstanceBlockStatus (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x7C

    status: TextComponent
    """Text Component"""

    has_size: Boolean
    """Boolean"""

    size_x: Double | None = None
    """OptionalDouble - Only present if Has Size is true."""

    size_y: Double | None = None
    """OptionalDouble - Only present if Has Size is true."""

    size_z: Double | None = None
    """OptionalDouble - Only present if Has Size is true."""
