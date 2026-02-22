from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import UUID, VarInt


class ResourcePackResponse(Packet, kw_only=True):
    """Packet representing ResourcePackResponse (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x30

    uuid: UUID
    """
    UUID - The unique identifier of the resource pack received in theAdd
    Resource Pack (play)request.
    """

    result: VarInt
    """VarIntEnum - Result ID (see below)."""
