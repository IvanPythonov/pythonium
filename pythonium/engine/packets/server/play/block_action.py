from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Position, UByte, VarInt


class BlockAction(Packet, kw_only=True):
    """Packet representing BlockAction (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x07

    location: Position
    """Position - Block coordinates."""

    action_id_byte_1: UByte
    """
    Unsigned Byte - Varies depending on block — seeJava Edition
    protocol/Block actions.
    """

    action_parameter_byte_2: UByte
    """
    Unsigned Byte - Varies depending on block — seeJava Edition
    protocol/Block actions.
    """

    block_type: VarInt
    """
    VarInt - ID in theminecraft:blockregistry. This value is unused by the
    vanilla client, as it will infer the type of block based on the given
    position.
    """
