from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class PlaceGhostRecipe(Packet, kw_only=True):
    """Packet representing PlaceGhostRecipe (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x3D

    window_id: VarInt
    """VarInt"""

    recipe_display: Any  # TODO: Recipe Display
    """Recipe Display"""
