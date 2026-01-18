from typing import ClassVar, TypedDict

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets import Packet
from pythonium.engine.typealiases import TextComponent
from pythonium.engine.types import Long, VarInt


class VersionDict(TypedDict):
    """Dictionary for version information."""

    name: str
    protocol: int


class SamplePlayersDict(TypedDict):
    """Dictionary for sample player information."""

    name: str
    id: str


class PlayersDict(TypedDict):
    """Dictionary for player information."""

    max: int
    online: int
    sample: list[SamplePlayersDict]


class ServerStatus(Packet, kw_only=True):
    """Packet representing status."""

    __schema_as_json__ = True

    __state__ = State.STATUS
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x00

    version: VersionDict
    players: PlayersDict
    description: TextComponent

    favicon: str = "data:image/png;base64,<data>"
    enforcesSecureChat: bool = False  # noqa: N815


class Pong(Packet, kw_only=True):
    """Packet representing pong."""

    __state__ = State.STATUS
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x01

    time: Long
