from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class ConfirmTeleportation(Packet, kw_only=True):
    """Packet representing ConfirmTeleportation (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x00

    teleport_id: VarInt
    """VarInt - The ID given by theSynchronize Player Positionpacket."""
