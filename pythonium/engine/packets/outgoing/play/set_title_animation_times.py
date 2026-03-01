from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Int, VarInt


class SetTitleAnimationTimes(Packet, kw_only=True):
    """Packet representing SetTitleAnimationTimes (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x71

    fade_in: Int
    """Int - Ticks to spend fading in."""

    stay: Int
    """Int - Ticks to keep the title displayed."""

    fade_out: Int
    """Int - Ticks to spend fading out, not when to start fading out."""
