"""Move Player Rot realization Router."""

from pythonium.engine.packets import (
    PlayerRotation,
)
from pythonium.server.routers.play import router as play_router


@play_router.on(PlayerRotation)
async def on_move_player_rot(move_player_rot: PlayerRotation) -> None:
    pass
