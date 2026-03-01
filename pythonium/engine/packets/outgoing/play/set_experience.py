from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Float, VarInt


class SetExperience(Packet, kw_only=True):
    """Packet representing SetExperience (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x65

    experience_bar: Float
    """Float - Between 0 and 1."""

    level: VarInt
    """VarInt"""

    total_experience: VarInt
    """
    VarInt - SeeExperience#Leveling upon the Minecraft Wiki for Total
    Experience to Level conversion.
    """
