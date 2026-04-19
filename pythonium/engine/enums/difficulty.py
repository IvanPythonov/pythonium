from enum import IntEnum, unique

from pythonium.engine.codecs import UnsignedByteCodec


@unique
class DifficultyEnum(IntEnum):
    """Game difficulty levels."""

    __codec__ = UnsignedByteCodec()

    PEACEFUL = 0
    """Peaceful"""

    EASY = 1
    """Easy"""

    NORMAL = 2
    """Normal"""

    HARD = 3
    """Hard"""
