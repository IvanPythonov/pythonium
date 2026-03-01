from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import NBTCompound, VarInt


class TagQueryResponse(Packet, kw_only=True):
    """Packet representing TagQueryResponse (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x79

    transaction_id: VarInt
    """
    VarInt - Can be compared to the one sent in the original query packet.
    """

    nbt: NBTCompound
    """
    NBT - The NBT of the block or entity. May be a TAG_END (0), in which
    case no NBT is present.
    """
