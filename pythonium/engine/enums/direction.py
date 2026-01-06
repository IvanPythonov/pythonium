from enum import IntEnum, auto, unique


@unique
class Direction(IntEnum):
    """Enum class representing direction of packet."""

    SERVERBOUND = auto()
    CLIENTBOUND = auto()
