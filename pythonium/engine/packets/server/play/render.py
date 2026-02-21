from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets import Packet
from pythonium.engine.types import (
    VarInt,
)


class SetSimulationDistance(Packet, kw_only=True):
    """Packet representing set simulation distance."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x6D

    simulation_distance: VarInt


class SetRenderDistance(Packet, kw_only=True):
    """Packet representing set render distance."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x57

    view_distance: VarInt
