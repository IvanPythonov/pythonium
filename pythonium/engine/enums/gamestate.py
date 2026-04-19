from enum import IntEnum, unique

from pythonium.engine.codecs import VarIntCodec


@unique
class GameStateReason(IntEnum):
    """Game state change reasons."""

    __codec__ = VarIntCodec()

    NO_RESPAWN_BLOCK = 0
    """No respawn block available"""

    BEGIN_RAIN = 1
    """Begin raining"""

    END_RAIN = 2
    """End raining"""

    CHANGE_GAME_MODE = 3
    """Change game mode"""

    WIN_GAME = 4
    """Win game"""

    DEMO_EVENT = 5
    """Demo event"""

    ARROW_HIT_PLAYER = 6
    """Arrow hit player"""

    RAIN_LEVEL_CHANGE = 7
    """Rain level change"""

    THUNDER_LEVEL_CHANGE = 8
    """Thunder level change"""

    PUMFFERFISH_STING_SOUND = 9
    """Pufferfish sting sound"""

    ELDER_GUARDIAN_APPEARANCE = 10
    """Elder guardian appearance"""

    ENABLE_RESPAWN_SCREEN = 11
    """Enable respawn screen"""

    LIMITED_CRAFTING = 12
    """Limited crafting"""

    START_WAITING_FOR_CHUNKS = 13
    """Start waiting for level chunks"""
