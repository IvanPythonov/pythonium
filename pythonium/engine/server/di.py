from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from pythonium.engine.entity.tracker import EntityTracker
from pythonium.engine.properties_reader import Properties
from pythonium.engine.server.client_manager import ClientManager
from pythonium.engine.services.player_world_view import WorldViewService
from pythonium.engine.ticker import Ticker
from pythonium.engine.world import World
from pythonium.worldgen.chunk_sender import ChunkSender

if TYPE_CHECKING:
    from pythonium.engine import Client, Server


@dataclass
class Container:
    """Container."""

    properties: Properties
    client_manager: ClientManager
    world: World
    entity_tracker: EntityTracker
    chunk_sender: ChunkSender
    world_view_service: WorldViewService
    server: Server
    ticker: Ticker

    extra: dict[str, Any] = field(default_factory=dict)

    def register(self, name: str, value: object) -> None:
        self.extra[name] = value

    def resolve_kwargs(
        self,
        needed_params: frozenset[str],
        client: Client | None = None,
    ) -> dict[str, Any]:
        mapping: dict[str, Any] = {
            "properties": self.properties,
            "client_manager": self.client_manager,
            "clients": self.client_manager,
            "world": self.world,
            "entity_tracker": self.entity_tracker,
            "chunk_sender": self.chunk_sender,
            "world_view_service": self.world_view_service,
            "server": self.server,
            "ticker": self.ticker,
            **self.extra,
        }

        if client is not None:
            mapping["client"] = client

        return {
            name: val for name, val in mapping.items() if name in needed_params
        }
