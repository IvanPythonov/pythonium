from typing import ClassVar

from pythonium.engine.enums import Direction, State, TeleportFlags
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Double, Float, VarInt


class SynchronizePlayerPosition(Packet, kw_only=True):
    """Packet representing SynchronizePlayerPosition (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x41

    teleport_id: VarInt
    """
    VarInt - Client should confirm this packet withConfirm
    Teleportationcontaining the same Teleport ID.
    """

    x: Double
    """Double - Absolute or relative position, depending on Flags."""

    y: Double
    """Double - Absolute or relative position, depending on Flags."""

    z: Double
    """Double - Absolute or relative position, depending on Flags."""

    velocity_x: Double
    """Double"""

    velocity_y: Double
    """Double"""

    velocity_z: Double
    """Double"""

    yaw: Float
    """Float - Absolute or relative rotation on the X axis, in degrees."""

    pitch: Float
    """Float - Absolute or relative rotation on the Y axis, in degrees."""

    flags: TeleportFlags
    """Teleport Flags"""
