from enum import IntEnum, unique

from pythonium.engine.codecs import VarIntCodec


@unique
class BlockActionStatus(IntEnum):
    """Block action status."""

    __codec__ = VarIntCodec()

    CLEARED = 0
    RUNNING = 1
    FINISHED = 2


@unique
class Rotation(IntEnum):
    """Rotation."""

    __codec__ = VarIntCodec()

    NONE = 0
    CLOCKWISE_90 = 1
    CLOCKWISE_180 = 2
    COUNTER_CLOCKWISE_90 = 3


@unique
class BlockAction(IntEnum):
    """Block action."""

    __codec__ = VarIntCodec()

    PASS = 0
