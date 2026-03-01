from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class SetRenderDistance(Packet, kw_only=True):
    """Packet representing SetRenderDistance (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x5D

    view_distance: VarInt
    """VarInt - Render distance (2-32)."""
