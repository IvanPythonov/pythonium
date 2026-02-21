import socket
from asyncio import StreamReader, StreamWriter, start_server
from collections.abc import Iterable, Sized
from logging import getLogger

from pythonium.engine import Client, Router
from pythonium.engine.client import ClientConnection, ClientSession
from pythonium.engine.enums import State
from pythonium.engine.packets import serialize
from pythonium.engine.server import PacketReader

logger = getLogger(__name__)


class Server:
    """Class representing Minecraft server."""

    def __init__(
        self, host: str = "127.0.0.1", port: int = 25565, **kwargs: object
    ) -> None:
        self._clients: list[Client] = []

        self.host = host
        self.port = port

        self.router = Router(name=self.__class__.__name__, kwargs=kwargs)

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
        client_socket = writer.get_extra_info("socket")
        if client_socket is not None:
            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            client_socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_RCVBUF, 65536
            )
            client_socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_SNDBUF, 65536
            )

        address = writer.get_extra_info("peername")[0]
        logger.info("New connection from %s", address)

        client = Client(
            ClientConnection(reader=reader, writer=writer),
            ClientSession(state=State.HANDSHAKING),
        )

        packet_reader = PacketReader(reader)

        async for packet in packet_reader.read(client_session=client.session):
            logger.debug(packet)
            logger.info(
                "Received packet with ID %s", f"{packet.packet_id:#04x}"
            )

            server_packet = await self.router.route(packet, client=client)

            logger.debug(packet)

            if not server_packet:
                continue

            logger.debug(server_packet)

            if isinstance(server_packet, Iterable) and isinstance(
                server_packet, Sized
            ):
                logger.info(
                    "Sending %d packets to %s",
                    len(server_packet),
                    address,
                )

                for packet_ in server_packet:
                    serialized_packet = serialize(packet_)
                    logger.debug(serialized_packet)

                    await client.connection.write(serialized_packet)

            else:
                serialized_packet = serialize(server_packet)
                logger.debug(serialized_packet)

                await client.connection.write(serialized_packet)

        self.remove_client(client)
        logger.info("Disconnected from %s", address)
        await client.connection.disconnect()

    async def serve(self) -> None:
        server = await start_server(
            self._handle_connection, self.host, self.port
        )

        logger.info("Serving on %s:%s", self.host, self.port)

        async with server:
            await server.serve_forever()
