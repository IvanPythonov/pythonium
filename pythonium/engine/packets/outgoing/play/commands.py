from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class Commands(Packet, kw_only=True):
    """Packet representing Commands (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x10

    nodes: Any  # TODO: Prefixed ArrayofNode
    """Prefixed ArrayofNode - An array of nodes."""

    root_index: VarInt
    """VarInt - Index of therootnode in the previous array."""
