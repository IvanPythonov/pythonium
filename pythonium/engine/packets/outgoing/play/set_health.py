from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Float, VarInt


class SetHealth(Packet, kw_only=True):
    """Packet representing SetHealth (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x66

    health: Float
    """Float - 0 or less = dead, 20 = full HP."""

    food: VarInt
    """VarInt - 0–20."""

    food_saturation: Float
    """Float - Seems to vary from 0.0 to 5.0 in integer increments."""
