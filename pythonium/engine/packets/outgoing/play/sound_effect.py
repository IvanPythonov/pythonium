from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Float, Int, Long, VarInt


class SoundEffect(Packet, kw_only=True):
    """Packet representing SoundEffect (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x73

    sound_event: Any  # TODO: ID orSound Event
    """
    ID orSound Event - ID in theminecraft:sound_eventregistry, or an inline
    definition.
    """

    sound_category: VarInt
    """
    VarIntEnum - The category that this sound will be played from (current
    categories).
    """

    effect_position_x: Int
    """
    Int - Effect X multiplied by 8 (fixed-point numberwith only 3 bits
    dedicated to the fractional part).
    """

    effect_position_y: Int
    """
    Int - Effect Y multiplied by 8 (fixed-point numberwith only 3 bits
    dedicated to the fractional part).
    """

    effect_position_z: Int
    """
    Int - Effect Z multiplied by 8 (fixed-point numberwith only 3 bits
    dedicated to the fractional part).
    """

    volume: Float
    """Float - 1.0 is 100%, capped between 0.0 and 1.0 by vanilla clients."""

    pitch: Float
    """Float - Float between 0.5 and 2.0 by vanilla clients."""

    seed: Long
    """Long - Seed used to pick sound variant."""
