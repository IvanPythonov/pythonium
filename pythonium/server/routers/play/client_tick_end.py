"""Client Tick End realization Router."""

from pythonium.engine.packets.ingoing import (
    TickEnd,
)
from pythonium.engine.router import Router

router = Router(name=__name__)


@router.on(TickEnd)
async def on_tick_end(client_tick_end: TickEnd) -> None:
    pass
