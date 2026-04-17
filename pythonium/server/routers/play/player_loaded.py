"""Player Loaded Event realization Router."""

from pythonium.engine.packets.ingoing import (
    PlayerLoaded,
)
from pythonium.server.routers.play import router as play_router


@play_router.on(PlayerLoaded)
async def on_player_loaded(
    player_loaded: PlayerLoaded,
) -> None:
    pass
