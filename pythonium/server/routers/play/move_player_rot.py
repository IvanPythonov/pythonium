"""Move Player Rot realization Router."""

from pythonium.engine.packets.ingoing import (
    PositionLook,
)
from pythonium.server.routers.play import router as play_router


@play_router.on(PositionLook)
async def on_move_player_rot(move_player_rot: PositionLook) -> None:
    pass
