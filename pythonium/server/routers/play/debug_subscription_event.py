"""Debug Subscription Event realization Router."""

from pythonium.engine.packets.ingoing import (
    DebugSampleSubscription,
)
from pythonium.server.routers.play import router as play_router


@play_router.on(DebugSampleSubscription)
async def on_debug_event(
    debug_event: DebugSampleSubscription,
) -> None:
    pass
