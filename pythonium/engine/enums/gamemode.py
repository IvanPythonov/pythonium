from enum import IntEnum, unique

from pythonium.engine.codecs import VarIntCodec


@unique
class GameMode(IntEnum):
    """Player game mode."""

    __codec__ = VarIntCodec()

    SURVIVAL = 0
    """Survival"""

    CREATIVE = 1
    """Creative"""

    ADVENTURE = 2
    """Adventure"""

    SPECTATOR = 3
    """Spectator"""
