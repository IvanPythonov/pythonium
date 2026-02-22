from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, VarInt


class PlaceRecipe(Packet, kw_only=True):
    """Packet representing PlaceRecipe (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x26

    window_id: VarInt
    """VarInt"""

    recipe_id: VarInt
    """VarInt - ID of recipe previously defined inRecipe Book Add."""

    make_all: Boolean
    """
    Boolean - Affects the amount of items processed; true if shift is down
    when clicked.
    """
