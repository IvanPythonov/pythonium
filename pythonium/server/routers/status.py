"""Status Phase Router."""

from pythonium.engine import Router
from pythonium.engine.client import Client
from pythonium.engine.packets import GetStatus, Ping, Pong, ServerStatus
from pythonium.engine.properties_reader import Properties

router = Router(name=__name__)

PROTOCOL_VERSION = {
    "1.21.8": 772,
}


@router.on(GetStatus)
async def on_status(
    _status: GetStatus, properties: Properties, client: Client
) -> None:
    await client.send(
        ServerStatus(
            version={
                "name": properties.server.version,
                "protocol": PROTOCOL_VERSION[properties.server.version],
            },
            players={
                "max": properties.server.max_players,
                "online": 1,
                "sample": [
                    {
                        "name": "thanks_wiki_vg",
                        "id": "4566e69f-c907-48ee-8d71-d7ba5aa00d20",
                    }
                ],
            },
            description={"text": properties.server.motd},
        )
    )


@router.on(Ping)
async def on_ping(ping: Ping, client: Client) -> None:
    await client.send(Pong(time=ping.time))
