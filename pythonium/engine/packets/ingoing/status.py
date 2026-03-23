from typing import ClassVar

from pythonium.engine.packets.base import Packet
from pythonium.engine.types import (
    Long,
)


class PingStart(Packet, kw_only=True):
    """Packet representing PingStart."""

    __packet_name__: ClassVar[str] = "status:serverbound:ping_start"


class Ping(Packet, kw_only=True):
    """Packet representing Ping."""

    __packet_name__: ClassVar[str] = "status:serverbound:ping"

    time: Long
