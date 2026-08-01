import asyncio

from pythonium.engine import Client
from pythonium.engine.exceptions import EmptyBroadcastError
from pythonium.engine.packets import Packet
from pythonium.engine.server.client_manager import ClientManager


class Network:
    """Network."""

    def __init__(
        self,
        client_manager: ClientManager,
    ) -> None:
        self.client_manager = client_manager

    async def _send_packets_to_client(
        self, client: Client, packets: tuple[Packet, ...]
    ) -> None:
        for packet in packets:
            await client.send(packet)

    async def broadcast(self, packet: Packet) -> None:
        await self.broadcast_many(packet)

    async def broadcast_many(self, *packets: Packet) -> None:
        if not packets:
            raise EmptyBroadcastError(packets=packets)

        await asyncio.gather(
            *(
                self._send_packets_to_client(client, packets)
                for client in self.client_manager
            ),
            return_exceptions=True,
        )
