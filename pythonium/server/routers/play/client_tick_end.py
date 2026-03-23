"""Client Tick End realization Router."""

from pythonium.engine.packets.ingoing import (
    TickEnd,
)
from pythonium.server.routers.play import router as play_router


@play_router.on(TickEnd)
async def on_tick_end(client_tick_end: TickEnd) -> None:
    pass
