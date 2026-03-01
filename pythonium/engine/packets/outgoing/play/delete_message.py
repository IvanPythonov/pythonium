from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class DeleteMessage(Packet, kw_only=True):
    """Packet representing DeleteMessage (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x1F

    message_id: VarInt
    """
    VarInt - The message ID + 1, used for validating message signature. The
    next field is present only when value of this field is equal to 0.
    """

    signature: Any  # TODO: Byte Array| None = None
    """
    OptionalByte Array(256) - The previous message's signature. Always 256
    bytes and not length-prefixed.
    """
