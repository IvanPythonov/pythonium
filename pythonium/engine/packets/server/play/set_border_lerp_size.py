from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Double, VarInt, VarLong


class SetBorderLerpSize(Packet, kw_only=True):
    """Packet representing SetBorderLerpSize (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x57

    old_diameter: Double
    """
    Double - Current length of a single side of the world border, in
    meters.
    """

    new_diameter: Double
    """
    Double - Target length of a single side of the world border, in meters.
    """

    speed: VarLong
    """
    VarLong - Number of real-timemilliseconds until New Diameter is
    reached. It appears that vanilla server does not sync world border
    speed to game ticks, so it gets out of sync with server lag. If the
    world border is not moving, this is set to 0.
    """
