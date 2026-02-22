from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Byte, Identifier, VarInt


class StopSound(Packet, kw_only=True):
    """Packet representing StopSound (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x75

    flags: Byte
    """Byte - Controls which fields are present."""

    source: VarInt
    """
    OptionalVarIntEnum - Only if flags is 3 or 1 (bit mask 0x1). See below.
    If not present, then sounds from all sources are cleared.
    """

    sound: Identifier | None = None
    """
    OptionalIdentifier - Only if flags is 2 or 3 (bit mask 0x2).  A sound
    effect name, seeCustom Sound Effect. If not present, then all sounds
    are cleared.
    """
