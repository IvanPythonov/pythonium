"""Player Input Event realization Router."""

from pythonium.engine.packets.ingoing.play import PlayerInput
from pythonium.engine.router import Router

router = Router(name=__name__)


@router.on(PlayerInput)
async def on_player_input(
    player_input: PlayerInput,
) -> None:
    pass
