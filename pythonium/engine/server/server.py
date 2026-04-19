import asyncio
import os
import socket
from asyncio import (
    StreamReader,
    StreamWriter,
    gather,
    start_server,
)
from logging import getLogger

from pythonium.engine import Client, Router
from pythonium.engine.client import ClientConnection, ClientSession
from pythonium.engine.enums import State
from pythonium.engine.packets.base import Packet
from pythonium.engine.properties_reader import Properties, get_properties
from pythonium.engine.server import PacketReader
from pythonium.engine.tasks.keepalive import send_keepalive
from pythonium.engine.ticker.ticker import Ticker
from pythonium.engine.world import World

logger = getLogger(__name__)


def exception_task_handler(task: asyncio.Task) -> None:
    task.result()


async def safe_route(
    router: Router,
    packet: Packet,
    client: Client,
    properties: Properties,
) -> None:
    try:
        await router.route(packet=packet, client=client)
    except Exception as e:
        error = "Internal Server Error."
        if properties.server.debug or getattr(e, "show_in_production", False):
            error += f"\n\u00a7c Details: {e!r}"
        await client.kick(error)
        raise


class Server:
    """Class representing Minecraft server."""

    def __init__(self, **kwargs: object) -> None:
        self._clients: set[Client] = set()

        self.properties = get_properties(path="properties.toml")

        self.world = World()
        self.ticker = Ticker(world=self.world)

        self.router = Router(name=self.__class__.__name__, kwargs=kwargs)

    def add_client(self, client: Client) -> None:
        """Add a client to the server."""
        self._clients.add(client)

    def remove_client(self, client: Client) -> None:
        """Remove a client from the server."""
        self._clients.discard(client)

    async def broadcast(self, packet: Packet) -> None:
        await asyncio.gather(
            *(client.send(packet) for client in self._clients)
        )

    async def broadcast_many(self, *packets: Packet) -> None:
        for packet in packets:
            await self.broadcast(packet=packet)

    def _configure_socket(self, writer: StreamWriter) -> None:
        client_socket: socket.socket = writer.get_extra_info("socket")
        if not client_socket:
            return

        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        if hasattr(socket, "TCP_QUICKACK"):
            client_socket.setsockopt(
                socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1
            )

        client_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_SNDBUF, 128 * 1024
        )
        client_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_RCVBUF, 128 * 1024
        )

        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        writer.transport.set_write_buffer_limits(high=64 * 1024)

    async def _handle_connection(
        self, reader: StreamReader, writer: StreamWriter
    ) -> None:
        """Handle a new client connection."""
        self._configure_socket(writer=writer)

        address: str = writer.get_extra_info("peername")[0]
        logger.info("New connection from %s", address)

        client = Client(
            ClientConnection(reader=reader, writer=writer),
            ClientSession(state=State.HANDSHAKING),
        )

        self.add_client(client)

        keepalive_task = asyncio.create_task(
            send_keepalive(client=client),
            name=f"KeepAliveTask-{address}",
        )

        packet_reader = PacketReader(reader)

        async for packet in packet_reader.read(client_session=client.session):
            await safe_route(
                packet=packet,
                router=self.router,
                client=client,
                properties=self.properties,
            )

        keepalive_task.cancel()
        self.remove_client(client)
        logger.info("Disconnected from %s", address)
        await client.disconnect()

    async def serve(self) -> None:
        logger.info(
            "Serving on %s:%s",
            self.properties.server.host,
            self.properties.server.port,
        )
        logger.debug("Current PID: %d", os.getpid())

        self.router.bake(
            ticker=self.ticker,
            properties=self.properties,
            world=self.world,
        )

        ticker = self.ticker.run()
        server = start_server(
            self._handle_connection,
            self.properties.server.host,
            self.properties.server.port,
        )

        await gather(ticker, server)
