"""Abilities Router."""

from pythonium.engine.packets.ingoing.play import Abilities
from pythonium.engine.router import Router

router = Router(name=__name__)


@router.on(Abilities)
async def abilities_handler(abilities: Abilities) -> None:
    pass
