from enum import IntFlag, unique

from pythonium.engine.codecs import ByteCodec


@unique
class PlacementFlags(IntFlag):
    """Block placement flags bitmask."""

    __codec__ = ByteCodec()

    IGNORE_ENTITIES = 0x01
    """Ignore entities"""

    SHOW_AIR = 0x02
    """Show air"""

    SHOW_BOUNDING_BOX = 0x04
    """Show bounding box"""

    STRICT_PLACEMENT = 0x08
    """Strict placement"""
