import asyncio
import socket
from asyncio import StreamReader, StreamWriter

from pythonium.engine import Client
from pythonium.engine.factories.client import build_client
from pythonium.engine.packets.base import bake_all_packets
from pythonium.engine.properties_reader import Properties
from pythonium.engine.server import PacketReader
from pythonium.engine.server.client_manager import ClientManager
from pythonium.engine.server.packet_dispatcher import PacketDispatcher
from pythonium.engine.tasks.keepalive import send_keepalive
from pythonium.server.routers.play.keepalive import keep_alive_handler


class NetworkHandler:
    """Network handler."""

    def __init__(
        self,
        host: str,
        port: int,
        client_manager: ClientManager,
        properties: Properties,
        packet_dispatcher: PacketDispatcher,
    ) -> None:
        self.host = host
        self.port = port

        self.client_manager = client_manager
        self.properties = properties

        self.packet_dispatcher = packet_dispatcher

        bake_all_packets()

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

    async def on_connect(
        self, reader: StreamReader, writer: StreamWriter
    ) -> None:
        self._configure_socket(writer=writer)

        address = writer.get_extra_info("peername")[0]

        client = build_client(reader=reader, writer=writer)

        keepalive_task = asyncio.create_task(
            send_keepalive(client=client),
            name=f"KeepAliveTask-{address}",
        )
        client.session.background_tasks.add(keepalive_task)
        keepalive_task.add_done_callback(
            client.session.background_tasks.discard
        )

        self.client_manager.add(client)

        packet_reader = PacketReader(reader)

        try:
            async for packet in packet_reader.read(
                client_session=client.session
            ):
                await self.packet_dispatcher.dispatch(packet, client=client)
        except Exception as exception:
            await self._kick_on_exception(client, exception)
            raise
        finally:
            self.client_manager.remove(client)
            await client.disconnect()

    async def _kick_on_exception(
        self, client: Client, exception: Exception
    ) -> None:
        error = "Internal Server Error."
        if self.properties.server.debug or getattr(
            exception, "show_in_production", False
        ):
            error += f"\n\u00a7c Details: {exception!r}"
        await client.kick(error)
