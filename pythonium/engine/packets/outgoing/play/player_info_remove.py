from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class PlayerInfoRemove(Packet, kw_only=True):
    """Packet representing PlayerInfoRemove (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x43

    uuids: Any  # TODO: Prefixed ArrayofUUID
    """Prefixed ArrayofUUID - UUIDs of players to remove."""
