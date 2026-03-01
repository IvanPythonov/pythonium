from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, VarInt


class RecipeBookSettings(Packet, kw_only=True):
    """Packet representing RecipeBookSettings (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x4A

    crafting_recipe_book_open: Boolean
    """
    Boolean - If true, then the crafting recipe book will be open when the
    player opens its inventory.
    """

    crafting_recipe_book_filter_active: Boolean
    """
    Boolean - If true, then the filtering option is active when the player
    opens its inventory.
    """

    smelting_recipe_book_open: Boolean
    """
    Boolean - If true, then the smelting recipe book will be open when the
    player opens its inventory.
    """

    smelting_recipe_book_filter_active: Boolean
    """
    Boolean - If true, then the filtering option is active when the player
    opens its inventory.
    """

    blast_furnace_recipe_book_open: Boolean
    """
    Boolean - If true, then the blast furnace recipe book will be open when
    the player opens its inventory.
    """

    blast_furnace_recipe_book_filter_active: Boolean
    """
    Boolean - If true, then the filtering option is active when the player
    opens its inventory.
    """

    smoker_recipe_book_open: Boolean
    """
    Boolean - If true, then the smoker recipe book will be open when the
    player opens its inventory.
    """

    smoker_recipe_book_filter_active: Boolean
    """
    Boolean - If true, then the filtering option is active when the player
    opens its inventory.
    """
