from asyncio import StreamReader, StreamWriter, start_server
from logging import getLogger

from pythonium.engine import Client, Router
from pythonium.engine.client import ClientConnection, ClientSession
from pythonium.engine.enums import State
from pythonium.engine.packets import serialize
from pythonium.engine.server import PacketReader

logger = getLogger(__name__)


class Server(Router):
    """Class representing Minecraft server."""

    def __init__(
        self, host: str = "127.0.0.1", port: int = 25565, **kwargs: object
    ) -> None:
        super().__init__(name=self.__class__.__name__, kwargs=kwargs)

        self._clients: list[Client] = []

        self.host = host
        self.port = port

    def add_client(self, client: Client) -> None:
        """Add a client to the server."""
        self._clients.append(client)

    def remove_client(self, client: Client) -> None:
        """Remove a client from the server."""
        if client in self._clients:
            self._clients.remove(client)

    async def _handle_connection(
        self, reader: StreamReader, writer: StreamWriter
    ) -> None:
        """Handle a new client connection."""
        addr = writer.get_extra_info("peername")[0]
        logger.info("New connection from %s", addr)

        client = Client(
            ClientConnection(reader=reader, writer=writer),
            ClientSession(state=State.HANDSHAKING),
        )

        packet_reader = PacketReader(reader)

        async for packet in packet_reader.read(client_session=client.session):
            server_packet = await self.route(packet, client=client)
            if not server_packet:
                continue

            serialized_packet = serialize(server_packet)

            await client.connection.write(serialized_packet)

            logger.info("Received packet with ID %s", hex(packet.packet_id))

        self.remove_client(client)
        logger.info("Disconnected from %s", addr)
        await client.connection.disconnect()

    async def serve(self) -> None:
        server = await start_server(
            self._handle_connection, self.host, self.port
        )

        logger.info("Serving on %s:%s", self.host, self.port)

        async with server:
            await server.serve_forever()
