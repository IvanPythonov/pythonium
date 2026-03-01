from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class SetSeenRecipe(Packet, kw_only=True):
    """Packet representing SetSeenRecipe (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x2E

    recipe_id: VarInt
    """VarInt - ID of recipe previously defined in Recipe Book Add."""
