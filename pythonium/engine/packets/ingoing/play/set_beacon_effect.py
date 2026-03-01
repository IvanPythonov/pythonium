from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class SetBeaconEffect(Packet, kw_only=True):
    """Packet representing SetBeaconEffect (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x33

    primary_effect: VarInt | None = None
    """Prefixed OptionalVarInt - APotion ID."""

    secondary_effect: VarInt | None = None
    """Prefixed OptionalVarInt - APotion ID."""
