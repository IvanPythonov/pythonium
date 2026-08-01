"""Move Player Rot realization Router."""

from pythonium.engine.client.client import Client
from pythonium.engine.packets.ingoing import (
    PositionLook,
)
from pythonium.engine.packets.ingoing.play import Flying, Look, Position
from pythonium.engine.router import Router
from pythonium.engine.services.player_world_view import WorldViewService

router = Router(name=__name__)


@router.on(Position, PositionLook)
async def on_move_player(
    position: Position | PositionLook,
    client: Client,
    world_view_service: WorldViewService,
) -> None:
    position_x = int(position.x)
    position_z = int(position.z)

    await world_view_service.update_position(
        client=client, x=position_x, z=position_z
    )


@router.on(Flying)
async def on_flying(flying: Flying) -> None: ...


@router.on(Look)
async def on_look(look: Look) -> None: ...
