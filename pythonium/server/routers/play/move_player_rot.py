"""Move Player Rot realization Router."""

from pythonium.engine.packets import (
    MovePlayerRot,
)
from pythonium.server.routers.play import router as play_router


@play_router.on(MovePlayerRot)
async def on_move_player_rot(client_information: MovePlayerRot) -> None: ...
