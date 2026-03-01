from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class ChangeGameMode(Packet, kw_only=True):
    """Packet representing ChangeGameMode (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x04

    game_mode: VarInt
    """VarIntEnum - 0: survival, 1: creative, 2: adventure, 3: spectator."""
