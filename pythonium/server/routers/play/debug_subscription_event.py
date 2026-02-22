"""Debug Subscription Event realization Router."""

from pythonium.engine.packets import (
    DebugSubscriptionEvent,
)
from pythonium.server.routers.play import router as play_router


@play_router.on(DebugSubscriptionEvent)
async def on_move_player_rot(
    client_information: DebugSubscriptionEvent,
) -> None: ...
