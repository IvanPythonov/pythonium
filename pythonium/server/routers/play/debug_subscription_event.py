"""Debug Subscription Event realization Router."""

from pythonium.engine.packets.ingoing import (
    DebugSampleSubscription,
)
from pythonium.engine.router import Router

router = Router(name=__name__)


@router.on(DebugSampleSubscription)
async def on_debug_event(
    debug_event: DebugSampleSubscription,
) -> None:
    pass
