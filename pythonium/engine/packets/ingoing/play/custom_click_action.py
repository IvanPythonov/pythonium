from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Identifier, NBTCompound, VarInt


class CustomClickAction(Packet, kw_only=True):
    """Packet representing CustomClickAction (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x41

    id_: Identifier
    """Identifier - The identifier for the click action."""

    payload: NBTCompound
    """NBT - The data to send with the click action. May be a TAG_END (0)."""
