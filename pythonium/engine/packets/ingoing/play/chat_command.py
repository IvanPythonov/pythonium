from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import String, VarInt


class ChatCommand(Packet, kw_only=True):
    """Packet representing ChatCommand (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x06

    command: String
    """String(32767) - The command typed by the client excluding the/."""
