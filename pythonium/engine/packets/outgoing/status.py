from typing import ClassVar, TypedDict

from pythonium.engine.packets.base import Packet
from pythonium.engine.typealiases import TextComponent
from pythonium.engine.types import (
    Long,
)


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


class ServerInfo(Packet, kw_only=True, rename="camel"):
    """Packet representing ServerInfo."""

    __schema_as_json__: ClassVar[bool] = True
    __packet_name__: ClassVar[str] = "status:clientbound:server_info"

    version: VersionDict
    players: PlayersDict
    description: TextComponent

    favicon: str = "data:image/png;base64,<data>"
    enforces_secure_chat: bool = True


class Pong(Packet, kw_only=True):
    """Packet representing Pong."""

    __packet_name__: ClassVar[str] = "status:clientbound:ping"

    time: Long
