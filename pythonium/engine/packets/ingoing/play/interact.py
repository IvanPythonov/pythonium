from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Float, VarInt


class Interact(Packet, kw_only=True):
    """Packet representing Interact (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x19

    entity_id: VarInt
    """
    VarInt - The ID of the entity to interact. Note the special case
    described below.
    """

    type_: VarInt
    """VarIntEnum - 0: interact, 1: attack, 2: interact at."""

    target_x: Float | None = None
    """OptionalFloat - Only if Type is interact at."""

    target_y: Float | None = None
    """OptionalFloat - Only if Type is interact at."""

    target_z: Float | None = None
    """OptionalFloat - Only if Type is interact at."""

    hand: VarInt
    """
    OptionalVarIntEnum - Only if Type is interact or interact at; 0: main
    hand, 1: off hand.
    """

    sneak_key_pressed: Boolean
    """
    Boolean - If the client is pressing the sneak key. Has the same effect
    as a Player Command Press/Release sneak key preceding the interaction,
    and the state is permanently changed.
    """
