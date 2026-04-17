"""Player Input Event realization Router."""

from pythonium.engine.packets.ingoing.play import PlayerInput
from pythonium.server.routers.play import router as play_router


@play_router.on(PlayerInput)
async def on_player_input(
    player_input: PlayerInput,
) -> None:
    pass
