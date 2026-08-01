from enum import IntEnum, unique

from pythonium.engine.codecs import VarIntCodec


@unique
class PlayerActionStatus(IntEnum):
    """Player Action (BlockDig)."""

    __codec__ = VarIntCodec()

    START_DIGGING = 0
    CANCEL_DIGGING = 1
    FINISH_DIGGING = 2
    DROP_ITEM_STACK = 3
    DROP_ITEM = 4
    FINISH_ACTION = 5
    SWAP_ITEM = 6
