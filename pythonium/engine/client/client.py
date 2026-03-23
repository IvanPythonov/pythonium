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


class Client:
    """Class representing Minecraft client."""

    def __init__(
        self, connection: ClientConnection, session: ClientSession
    ) -> None:
        self.connection = connection
        self.session = session

        self.unique_id = connection.address

    async def kick(self, reason: str) -> None:
        reason_payload = {"text": String(reason)}
        packet: Packet | None = None

        match self.session.state:
            case State.LOGIN:
                packet = LoginDisconnect(reason=reason)
            case State.CONFIGURATION:
                packet = ConfigurationDisconnect(reason=reason_payload)
            case State.PLAY:
                packet = PlayDisconnect(reason=reason_payload)
            case _:
                raise KickError(
                    info="Wrong state (maybe status).",
                    state=self.session.state,
                )

        await self.connection.write(serialize(packet))

        await self.connection.disconnect()

    async def send(self, packet: Packet) -> None:
        await self.connection.write(serialize(packet))

    async def send_many(self, *packets: Packet) -> None:
        for packet in packets:
            await self.send(packet=packet)
