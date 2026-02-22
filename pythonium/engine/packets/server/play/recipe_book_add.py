from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Byte, VarInt


class RecipeBookAdd(Packet, kw_only=True):
    """Packet representing RecipeBookAdd (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x48

    recipes: Any  # TODO: Recipe ID
    """Recipe ID - Prefixed Array"""

    display: Any  # TODO: Recipe Display
    """Recipe Display"""

    group_id: VarInt
    """VarInt"""

    category_id: VarInt
    """VarInt - ID in theminecraft:recipe_book_categoryregistry."""

    ingredients: Any  # TODO: Prefixed ArrayofID Set| None = None
    """
    Prefixed OptionalPrefixed ArrayofID Set - IDs in
    theminecraft:itemregistry, or an inline definition.
    """

    flags: Byte
    """Byte - 0x01: show notification; 0x02: highlight as new"""

    replace: Boolean
    """Boolean - Replace or Add to known recipes"""
