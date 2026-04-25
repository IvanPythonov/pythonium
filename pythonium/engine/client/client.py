from collections.abc import Callable

from nbtlib import String

from pythonium.engine.client.connection import ClientConnection
from pythonium.engine.client.session import ClientSession
from pythonium.engine.enums.states import State
from pythonium.engine.exceptions import KickError
from pythonium.engine.packets.base import Packet, serialize
from pythonium.engine.packets.outgoing import (
    ConfigurationDisconnect,
    LoginDisconnect,
    PlayDisconnect,
)
from pythonium.engine.packets.outgoing.play import MultiBlockChange
from pythonium.worldgen.terrain.base import Chunk

_KICK_FACTORIES: dict[
    State,
    Callable[
        [str], LoginDisconnect | ConfigurationDisconnect | PlayDisconnect
    ],
] = {
    State.LOGIN: lambda reason: LoginDisconnect(reason=reason),
    State.CONFIGURATION: lambda reason: ConfigurationDisconnect(
        reason={"text": String(reason)}
    ),
    State.PLAY: lambda reason: PlayDisconnect(reason={"text": String(reason)}),
}


class Client:
    """Class representing Minecraft client."""

    def __init__(
        self, connection: ClientConnection, session: ClientSession
    ) -> None:
        self.connection = connection
        self.session = session

        self.unique_id = connection.address

    async def kick(self, reason: str) -> None:
        packet_factory = _KICK_FACTORIES.get(self.session.state)

        if not packet_factory:
            raise KickError(
                info="Wrong state for kicking (maybe status).",
                state=self.session.state,
            )

        packet = packet_factory(reason)

        await self.send(packet)
        await self.disconnect()

    async def send(self, packet: Packet) -> None:
        await self.connection.write(serialize(packet))

    async def send_many(self, *packets: Packet) -> None:
        for packet in packets:
            await self.send(packet=packet)

    async def disconnect(self) -> None:
        await self.connection.disconnect()
