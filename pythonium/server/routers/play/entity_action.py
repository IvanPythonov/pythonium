"""Entity Action Event realization Router."""

from pythonium.engine.packets.ingoing import (
    EntityAction,
)
from pythonium.engine.router import Router

router = Router(name=__name__)


@router.on(EntityAction)
async def on_entity_action(
    entity_action: EntityAction,
) -> None:
    pass
