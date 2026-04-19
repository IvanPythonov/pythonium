from enum import Enum, unique

from pythonium.engine.codecs.identifier import IdentifierCodec
from pythonium.engine.codecs.optional import OptionalCodec


@unique
class AdvancementRoot(Enum):
    """Advancement root identifiers."""

    __codec__: OptionalCodec = OptionalCodec(IdentifierCodec())

    STORY_ROOT = "minecraft:story/root"
    """Story root"""

    NETHER_ROOT = "minecraft:nether/root"
    """Nether root"""

    END_ROOT = "minecraft:end/root"
    """End root"""

    ADVENTURE_ROOT = "minecraft:adventure/root"
    """Adventure root"""

    HUSBANDRY_ROOT = "minecraft:husbandry/root"
    """Husbandry root"""
