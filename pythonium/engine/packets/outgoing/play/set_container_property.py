from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Short, VarInt


class SetContainerProperty(Packet, kw_only=True):
    """Packet representing SetContainerProperty (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x13

    window_id: VarInt
    """VarInt"""

    property: Short
    """Short - The property to be updated, see below."""

    value: Short
    """Short - The new value for the property, see below."""
