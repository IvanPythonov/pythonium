from enum import IntEnum, unique

from pythonium.engine.codecs import IntCodec


@unique
class TeleportFlags(IntEnum):
    """
    A bit field enum.

    In the lower 8 bits of the bit field,a set bit means the teleportation on
    the corresponding axis is relative, and an unset bit that it is absolute.
    """

    __codec__ = IntCodec()

    relative_x = 0x0001
    """Relative X"""
    relative_y = 0x0002
    """Relative Y"""
    relative_z = 0x0004
    """Relative Z"""
    relative_yaw = 0x0008
    """Relative Yaw"""
    relative_pitch = 0x0010
    """Relative Pitch"""
    relative_velocity_x = 0x0020
    """Relative Velocity X"""
    relative_velocity_y = 0x0040
    """Relative Velocity Y"""
    relative_velocity_z = 0x0080
    """Relative Velocity Z"""
    rotate_velocity = 0x0100
    """
    Rotate velocity according to the change in rotation, before applying the
    velocity change in this packet. Combining this with absolute rotation works
    as expected—the difference in rotation is still used.
    """
