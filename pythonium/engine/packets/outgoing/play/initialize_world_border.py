from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Double, VarInt, VarLong


class InitializeWorldBorder(Packet, kw_only=True):
    """Packet representing InitializeWorldBorder (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x2A

    x: Double
    """Double"""

    z: Double
    """Double"""

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

    portal_teleport_boundary: VarInt
    """
    VarInt - Resulting coordinates from a portal teleport are limited to
    ±value. Usually 29999984.
    """

    warning_blocks: VarInt
    """VarInt - In meters."""

    warning_time: VarInt
    """VarInt - In seconds as set by/worldborder warning time."""
