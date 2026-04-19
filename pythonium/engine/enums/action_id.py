from enum import IntEnum, unique

from pythonium.engine.codecs import VarIntCodec


@unique
class ActionId(IntEnum):
    """Player action identifiers."""

    __codec__ = VarIntCodec()

    LEAVE_BED = 0
    """Leave bed"""

    START_SPRINTING = 1
    """Start sprinting"""

    STOP_SPRINTING = 2
    """Stop sprinting"""

    START_JUMP_WITH_HORSE = 3
    """Start jump with horse"""

    STOP_JUMP_WITH_HORSE = 4
    """Stop jump with horse"""

    OPEN_VEHICLE_INVENTORY = 5
    """Open vehicle inventory"""

    START_FLYING_WITH_ELYTRA = 6
    """Start flying with elytra"""
