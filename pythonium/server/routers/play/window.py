"""Window realization Router."""

from pythonium.engine.packets.ingoing import CloseWindow
from pythonium.engine.router import Router

router = Router(name=__name__)


@router.on(CloseWindow)
async def on_close_window(
    close_window: CloseWindow,
) -> None:
    print(close_window)
