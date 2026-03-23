import asyncio
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
from pythonium.engine.properties_reader import get_properties
from pythonium.engine.server import PacketReader
from pythonium.engine.ticker.ticker import Ticker
from pythonium.engine.world import World

logger = getLogger(__name__)


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

    async def _handle_connection(
        self, reader: StreamReader, writer: StreamWriter
    ) -> None:
        """Handle a new client connection."""
        client_socket: socket.socket = writer.get_extra_info("socket")

        if client_socket is not None:
            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        address: str = writer.get_extra_info("peername")[0]
        logger.info("New connection from %s", address)

        client = Client(
            ClientConnection(reader=reader, writer=writer),
            ClientSession(state=State.HANDSHAKING),
        )

        packet_reader = PacketReader(reader)

        async for packet in packet_reader.read(client_session=client.session):
            logger.info(
                "Received packet with ID %s", f"{packet.packet_id:#04x}"
            )

            try:
                await self.router.route(
                    packet,
                    client=client,
                    ticker=self.ticker,
                    properties=self.properties,
                    world=self.world,
                )
            except Exception as e:
                if self.properties.server.debug:
                    await client.kick(str(e))
                logger.exception("Packet handle error")

        self.remove_client(client)
        logger.info("Disconnected from %s", address)
        await client.connection.disconnect()

    async def serve(self) -> None:
        logger.info(
            "Serving on %s:%s",
            self.properties.server.host,
            self.properties.server.port,
        )

        ticker = self.ticker.run()
        server = start_server(
            self._handle_connection,
            self.properties.server.host,
            self.properties.server.port,
        )

        await gather(ticker, server)
