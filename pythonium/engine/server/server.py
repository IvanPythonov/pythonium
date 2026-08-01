import asyncio

from pythonium.engine import Router
from pythonium.engine.entity.tracker import EntityTracker
from pythonium.engine.properties_reader import get_properties
from pythonium.engine.server.client_manager import ClientManager
from pythonium.engine.server.di import Container
from pythonium.engine.server.handler import NetworkHandler
from pythonium.engine.server.network import Network
from pythonium.engine.server.packet_dispatcher import PacketDispatcher
from pythonium.engine.services.player_world_view import WorldViewService
from pythonium.engine.ticker import Ticker
from pythonium.engine.world import World
from pythonium.worldgen.chunk_sender import ChunkSender
from pythonium.worldgen.terrain.flat import FlatWorldGenerator
from pythonium.worldgen.terrain.noise import NoiseWorldGenerator

CHUNK_GENERATORS = {
    "noise": NoiseWorldGenerator(),
    "flat": FlatWorldGenerator(),
}


class Server:
    """Server."""

    def __init__(self, **kwargs: object) -> None:
        self.properties = get_properties(path="properties.toml")
        self.router = Router(name=__name__)

        self.background_tasks = set()

        self.world = World(
            chunk_generator=CHUNK_GENERATORS[self.properties.world.world_type]
        )

        self.client_manager = ClientManager()

        self.network = Network(
            client_manager=self.client_manager,
        )

        self.chunk_sender = ChunkSender(world=self.world)
        self.world_view_service = WorldViewService(
            chunk_sender=self.chunk_sender,
            view_distance=self.properties.performance.view_distance,
        )

        self.entity_tracker = EntityTracker(
            network=self.network, world=self.world
        )

        self.ticker = Ticker(
            world=self.world, entity_tracker=self.entity_tracker
        )

        self.container = Container(
            properties=self.properties,
            client_manager=self.client_manager,
            world=self.world,
            entity_tracker=self.entity_tracker,
            world_view_service=self.world_view_service,
            server=self,
            chunk_sender=self.chunk_sender,
            ticker=self.ticker,
            extra=kwargs,
        )

        self.packet_dispatcher = PacketDispatcher(
            router=self.router, container=self.container
        )

        self.network_handler = NetworkHandler(
            host=self.properties.server.host,
            port=self.properties.server.port,
            client_manager=self.client_manager,
            properties=self.properties,
            packet_dispatcher=self.packet_dispatcher,
        )

    async def serve(self) -> None:
        self.router.bake()

        ticker_task = asyncio.create_task(self.ticker.run(), name="TickerTask")
        self.background_tasks.add(ticker_task)
        ticker_task.add_done_callback(self.background_tasks.discard)

        server = await asyncio.start_server(
            self.network_handler.on_connect,
            self.network_handler.host,
            self.network_handler.port,
        )

        async with server:
            await server.serve_forever()
