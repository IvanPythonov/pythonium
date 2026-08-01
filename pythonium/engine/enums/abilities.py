from enum import IntFlag, unique

from pythonium.engine.codecs import ByteCodec


@unique
class AbilitiesFlags(IntFlag):
    """Abilities flags."""

    __codec__ = ByteCodec()

    INVULNERABLE = 0x01
    """Invulnerable"""

    MAY_FLY = 0x02
    """May fly"""

    ALLOW_FLYING = 0x04
    """Allow flying"""

    INSTABREAK = 0x08
    """Instabreak"""

    CREATIVE = MAY_FLY | ALLOW_FLYING | INSTABREAK
    """Creative"""

    SURVIVAL = 0x00
    """Survival"""
