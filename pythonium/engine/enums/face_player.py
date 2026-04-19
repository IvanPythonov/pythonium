from enum import IntEnum, unique

from pythonium.engine.codecs.custom import VarIntCodec


@unique
class LookAt(IntEnum):
    """A look at enum."""

    __codec__ = VarIntCodec()

    eyes = 1
    """Aims using the head position"""
    feet = 0
    """Aims using the feet position. """
