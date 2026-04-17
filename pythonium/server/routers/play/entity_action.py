"""Entity Action Event realization Router."""

from pythonium.engine.packets.ingoing import (
    EntityAction,
)
from pythonium.server.routers.play import router as play_router


@play_router.on(EntityAction)
async def on_entity_action(
    entity_action: EntityAction,
) -> None:
    pass
