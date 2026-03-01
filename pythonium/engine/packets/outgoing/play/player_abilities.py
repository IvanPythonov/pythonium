from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Byte, Float, VarInt


class PlayerAbilities(Packet, kw_only=True):
    """Packet representing PlayerAbilities (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x3E

    flags: Byte
    """Byte - Bit field, see below."""

    flying_speed: Float
    """Float - 0.05 by default."""

    field_of_view_modifier: Float
    """
    Float - Modifies the field of view, like a speed potion. A vanilla
    server will use the same value as the movement speed sent in theUpdate
    Attributespacket, which defaults to 0.1 for players.
    """
