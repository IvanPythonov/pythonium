from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Identifier, VarInt


class SetCooldown(Packet, kw_only=True):
    """Packet representing SetCooldown (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x16

    cooldown_group: Identifier
    """
    Identifier - Identifier of the item (minecraft:stone) or the cooldown
    group ("use_cooldown" item component)
    """

    cooldown_ticks: VarInt
    """
    VarInt - Number of ticks to apply a cooldown for, or 0 to clear the
    cooldown.
    """
