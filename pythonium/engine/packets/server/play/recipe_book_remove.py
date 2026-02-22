from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class RecipeBookRemove(Packet, kw_only=True):
    """Packet representing RecipeBookRemove (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x49

    recipes: Any  # TODO: Prefixed ArrayofVarInt
    """Prefixed ArrayofVarInt - IDs of recipes to remove."""
