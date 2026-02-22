from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class ClientStatus(Packet, kw_only=True):
    """Packet representing ClientStatus (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x0B

    action_id: VarInt
    """VarIntEnum - See below"""
