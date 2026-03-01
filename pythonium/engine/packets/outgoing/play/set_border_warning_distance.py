from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class SetBorderWarningDistance(Packet, kw_only=True):
    """Packet representing SetBorderWarningDistance (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x5A

    warning_blocks: VarInt
    """VarInt - In meters."""
