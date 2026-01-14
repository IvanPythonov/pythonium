from enum import StrEnum, unique


@unique
class State(StrEnum):
    """Enum class representing states of a client."""

    OVERWORLD = "minecraft:overworld"
    NETHER = "minecraft:nether"
    END = "minecraft:the_end"
