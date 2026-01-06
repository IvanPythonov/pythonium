from enum import IntEnum, auto, unique


@unique
class State(IntEnum):
    """Enum class representing states of a client."""

    HANDSHAKING = auto()
    STATUS = auto()
    LOGIN = auto()
    CONFIGURATION = auto()
    PLAY = auto()
