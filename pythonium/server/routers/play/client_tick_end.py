"""Client Tick End realization Router."""

from pythonium.engine.packets import (
    ClientTickEnd,
)
from pythonium.server.routers.play import router as play_router


@play_router.on(ClientTickEnd)
async def on_tick_end(client_tick_end: ClientTickEnd) -> None:
    pass
