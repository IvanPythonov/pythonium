from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class SetEntityVelocity(Packet, kw_only=True):
    """Packet representing SetEntityVelocity (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x63

    entity_id: VarInt
    """VarInt"""

    velocity: Any  # TODO: LpVec3
    """LpVec3"""
