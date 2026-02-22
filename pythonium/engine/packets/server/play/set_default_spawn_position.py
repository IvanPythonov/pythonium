from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Float, Identifier, Position, VarInt


class SetDefaultSpawnPosition(Packet, kw_only=True):
    """Packet representing SetDefaultSpawnPosition (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x5F

    dimension_name: Identifier
    """Identifier - Name of spawn dimension."""

    location: Position
    """Position - Spawn location."""

    yaw: Float
    """Float - Yaw after respawning."""

    pitch: Float
    """Float - Pitch after respawning."""
