from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import NBTCompound, Position, VarInt


class BlockEntityData(Packet, kw_only=True):
    """Packet representing BlockEntityData (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x06

    location: Position
    """Position"""

    type_: VarInt
    """VarInt - ID in theminecraft:block_entity_typeregistry"""

    nbt_data: NBTCompound
    """NBT - Data to set."""
