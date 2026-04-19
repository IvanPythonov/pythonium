from enum import IntEnum, unique

from pythonium.engine.codecs import VarIntCodec


@unique
class UseEntityAction(IntEnum):
    """Entity interaction type."""

    __codec__ = VarIntCodec()

    INTERACT = 0
    """Interact"""

    ATTACK = 1
    """Attack"""

    INTERACT_AT = 2
    """Interact at position"""


@unique
class Hand(IntEnum):
    """Player hand selection."""

    __codec__ = VarIntCodec()

    MAIN_HAND = 0
    """Main hand"""

    OFF_HAND = 1
    """Off hand"""
