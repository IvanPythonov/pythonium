from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class SetCamera(Packet, kw_only=True):
    """Packet representing SetCamera (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x5B

    camera_id: VarInt
    """VarInt - ID of the entity to set the client's camera to."""
