from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Float, Position, VarInt


class SetDefaultSpawnPosition(Packet, kw_only=True):
    """Packet representing SetDefaultSpawnPosition (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x5A

    spawn_position: Position
    angle: Float
