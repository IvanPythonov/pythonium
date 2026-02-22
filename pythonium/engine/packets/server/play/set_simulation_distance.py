from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class SetSimulationDistance(Packet, kw_only=True):
    """Packet representing SetSimulationDistance (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x6D

    simulation_distance: VarInt
    """
    VarInt - The distance that the client will process specific things,
    such as entities.
    """
