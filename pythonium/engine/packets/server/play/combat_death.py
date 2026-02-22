from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import TextComponent, VarInt


class CombatDeath(Packet, kw_only=True):
    """Packet representing CombatDeath (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x42

    player_id: VarInt
    """
    VarInt - Entity ID of the player that died (should match the client's
    entity ID).
    """

    message: TextComponent
    """Text Component - The death message."""
