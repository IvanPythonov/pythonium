from pythonium.engine import Client, Router
from pythonium.engine.packets import Packet
from pythonium.engine.server.di import Container


class PacketDispatcher:
    """Packet dispatcher."""

    def __init__(self, router: Router, container: Container) -> None:
        self.container = container
        self.router = router

    async def dispatch(self, packet: Packet, client: Client) -> None:
        registry_handler = self.router.resolve_registry(type(packet))
        if registry_handler is not None:
            registries = await registry_handler(
                packet, container=self.container, client=client
            )
            if registries:
                await client.send_many(*registries)

        handler_struct = self.router.resolve_router(type(packet))
        if handler_struct is not None:
            await handler_struct(
                packet, container=self.container, client=client
            )
