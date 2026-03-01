from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import String, VarInt


class DisplayObjective(Packet, kw_only=True):
    """Packet representing DisplayObjective (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x60

    position: VarInt
    """
    VarInt - The position of the scoreboard. 0: list, 1: sidebar, 2: below
    name, 3 - 18: team-specific sidebar, indexed as 3 + team color.
    """

    score_name: String
    """String(32767) - The unique name for the scoreboard to be displayed."""
