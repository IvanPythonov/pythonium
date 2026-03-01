from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Byte, Int, VarInt


class EntityEvent(Packet, kw_only=True):
    """Packet representing EntityEvent (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x22

    entity_id: Int
    """Int"""

    entity_status: Byte
    """
    ByteEnum - SeeJava Edition protocol/Entity statusesfor a list of which
    statuses are valid for each type of entity.
    """
