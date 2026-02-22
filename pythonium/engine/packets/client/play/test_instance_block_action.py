from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import (
    Boolean,
    Identifier,
    Position,
    TextComponent,
    VarInt,
)


class TestInstanceBlockAction(Packet, kw_only=True):
    """Packet representing TestInstanceBlockAction (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x3E

    position: Position
    """Position"""

    action: VarInt
    """
    VarIntEnum - 0: init, 1: query, 2: set, 3: reset, 4: save, 5: export,
    6: run.
    """

    test: Identifier | None = None
    """
    Prefixed OptionalIdentifier - ID in theminecraft:test_instanceregistry.
    """

    size_x: VarInt
    """VarInt"""

    size_y: VarInt
    """VarInt"""

    size_z: VarInt
    """VarInt"""

    rotation: VarInt
    """
    VarIntEnum - 0: none, 1: clockwise 90°, 2: clockwise 180°, 3: counter-
    clockwise 90°.
    """

    ignore_entities: Boolean
    """Boolean"""

    status: VarInt
    """VarIntEnum - 0: cleared, 1: running, 2: finished."""

    error_message: TextComponent | None = None
    """Prefixed OptionalText Component"""
