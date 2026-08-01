from enum import IntEnum, unique

from pythonium.engine.codecs.custom import VarIntCodec


@unique
class BlockFace(IntEnum):
    """Block face directions."""

    __codec__ = VarIntCodec()

    DOWN = 0
    UP = 1

    NORTH = 2
    SOUTH = 3

    WEST = 4
    EAST = 5

    @property
    def offset(self) -> tuple[int, int, int]:
        return {
            BlockFace.DOWN: (0, -1, 0),
            BlockFace.UP: (0, 1, 0),
            BlockFace.NORTH: (0, 0, -1),
            BlockFace.SOUTH: (0, 0, 1),
            BlockFace.WEST: (-1, 0, 0),
            BlockFace.EAST: (1, 0, 0),
        }[self]
