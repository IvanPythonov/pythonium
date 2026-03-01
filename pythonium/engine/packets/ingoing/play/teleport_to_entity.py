from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import UUID, VarInt


class TeleportToEntity(Packet, kw_only=True):
    """Packet representing TeleportToEntity (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x3D

    target_player: UUID
    """
    UUID - UUID of the player to teleport to (can also be an entity UUID).
    """
