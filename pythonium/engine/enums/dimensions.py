from enum import StrEnum, unique


@unique
class Dimension(StrEnum):
    """Enum class representing dimensions."""

    OVERWORLD = "minecraft:overworld"
    NETHER = "minecraft:nether"
    END = "minecraft:the_end"
