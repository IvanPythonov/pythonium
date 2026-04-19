import asyncio
import secrets

from pythonium.engine.client.client import Client
from pythonium.engine.enums.states import State
from pythonium.engine.packets.base import Packet
from pythonium.engine.packets.outgoing import (
    ConfigurationKeepAlive,
    PlayKeepAlive,
)

_KEEPALIVE_FACTORY: dict[State, type[Packet]] = {
    State.CONFIGURATION: ConfigurationKeepAlive,
    State.PLAY: PlayKeepAlive,
}


async def send_keepalive(client: Client) -> None:
    while client.connection.is_connected:
        keepalive_packet = _KEEPALIVE_FACTORY.get(client.session.state)
        if keepalive_packet:
            await client.send(
                keepalive_packet(
                    keep_alive_id=secrets.randbelow(2**31 - 1)
                )
            )
        await asyncio.sleep(10)
