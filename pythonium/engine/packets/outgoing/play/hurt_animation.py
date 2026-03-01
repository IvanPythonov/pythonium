from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Float, VarInt


class HurtAnimation(Packet, kw_only=True):
    """Packet representing HurtAnimation (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x29

    entity_id: VarInt
    """VarInt - The ID of the entity taking damage"""

    yaw: Float
    """
    Float - The direction the damage is coming from in relation to the
    entity
    """
