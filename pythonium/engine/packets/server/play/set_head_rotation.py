from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Byte, VarInt


class SetHeadRotation(Packet, kw_only=True):
    """Packet representing SetHeadRotation (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x51

    entity_id: VarInt
    """VarInt"""

    head_yaw: Byte
    """Angle - New angle, not a delta."""
