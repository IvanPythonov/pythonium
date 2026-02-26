"""Debug Subscription Event realization Router."""

from pythonium.engine.packets import (
    DebugEvent,
)
from pythonium.server.routers.play import router as play_router


@play_router.on(DebugEvent)
async def on_move_player_rot(
    client_information: DebugEvent,
) -> None: ...
