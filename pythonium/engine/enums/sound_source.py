from enum import IntEnum, unique


@unique
class SoundSource(IntEnum):
    """Enum class representing sound sources."""

    MASTER = 0
    MUSIC = 1
    RECORD = 2
    WEATHER = 3
    BLOCK = 4
    HOSTILE = 5
    NEUTRAL = 6
    PLAYER = 7
    AMBIENT = 8
    VOICE = 9
    UI = 10
