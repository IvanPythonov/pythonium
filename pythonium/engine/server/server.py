from asyncio import StreamReader, StreamWriter, start_server
from logging import getLogger
from typing import ClassVar

from pythonium.engine import Client, Router
from pythonium.engine.client import ClientConnection, ClientSession
from pythonium.engine.codecs import VarIntCodec
from pythonium.engine.enums import Direction, State
from pythonium.engine.packets import deserialize, get_model_by_id
from pythonium.engine.server import PacketReader

logger = getLogger(__name__)


class Server(Router):
    """Class representing Minecraft server."""

    _clients: ClassVar[list[Client]] = []

    def __init__(
        self, host: str = "127.0.0.1", port: int = 25565, **kwargs: object
    ) -> None:
        super().__init__(name=self.__class__.__name__, kwargs=kwargs)
        self.host = host
        self.port = port

    def add_client(self, client: Client) -> None:
        """Add a client to the server."""
        self._clients.append(client)

    def remove_client(self, client: Client) -> None:
        """Remove a client from the server."""
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

        packet_data = await packet_reader.read_packet()
        packet_id, consumed = VarIntCodec().deserialize(packet_data)
        payload = packet_data[consumed:]

        model = get_model_by_id(
            packet_id=packet_id,
            state=client.session.state,
            direction=Direction.SERVERBOUND,
        )

        await super().route(
            deserialize(
                cls=model,
                data=packet_data,
            )
        )
        logger.info("Received packet with ID %s", hex(packet_id))

        # try:
        #     raise TypeError
        # except NotImplementedError:
        #     self.remove_client(client)
        #     logger.info("Disconnected from %s", addr)
        #     await client.disconnect()

    async def serve(self) -> None:
        server = await start_server(
            self._handle_connection, self.host, self.port
        )

        logger.info("Serving on %s:%s", self.host, self.port)

        async with server:
            await server.serve_forever()
