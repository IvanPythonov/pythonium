"""Some logic for router."""

from json import dumps

from pythonium.engine import Router
from pythonium.engine.packets import GetStatus, Ping, Pong, ServerStatus

router = Router(name=__name__)


@router.on(GetStatus)
async def on_status(_status: GetStatus) -> ServerStatus:
    return ServerStatus(
        json_response=dumps(
            {
                "version": {"name": "1.21.8", "protocol": 772},
                "players": {
                    "max": 100,
                    "online": 1,
                    "sample": [
                        {
                            "name": "thanks_wiki_vg",
                            "id": "4566e69f-c907-48ee-8d71-d7ba5aa00d20",
                        }
                    ],
                },
                "description": {"text": "Hello, world!"},
                "favicon": "data:image/png;base64,<data>",
                "enforcesSecureChat": False,
            }
        )
    )


@router.on(Ping)
async def on_ping(ping: Ping) -> Pong:
    return Pong(time=ping.time)
