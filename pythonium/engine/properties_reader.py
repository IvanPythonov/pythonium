from pathlib import Path
from typing import Literal

from msgspec import Struct, toml


class KebabStruct(Struct, rename="kebab"):
    """Base struct for auto renaming arguments."""


class ServerProperties(KebabStruct):
    """Server properties."""

    motd: str
    max_players: int
    version: str
    host: str
    port: int
    debug: bool


class AuthProperties(KebabStruct):
    """Authentification properties."""

    online_mode: bool
    connection_throttle: int


class WorldProperties(KebabStruct):
    """World properties."""

    gamemode: Literal["survival", "creative", "adventure", "spectator"]
    difficulty: Literal["peaceful", "easy", "normal", "hard"]
    seed: int
    hardcore: bool


class PerformanceProperties(KebabStruct):
    """Performance properties."""

    view_distance: int
    simulation_distance: int
    target_tps: int


class NetworkProperties(KebabStruct):
    """Network properties."""

    compression_threshold: int
    max_packet_size: int


class ChatProperties(KebabStruct):
    """Chat properties."""

    allow_colors: bool
    prevent_spam: bool


class Properties(KebabStruct):
    """Properties."""

    server: ServerProperties
    auth: AuthProperties
    world: WorldProperties
    performance: PerformanceProperties
    network: NetworkProperties
    chat: ChatProperties


def get_properties(path: Path | str) -> Properties:
    with Path(path).open("rb") as file:
        return toml.decode(file.read(), type=Properties)
