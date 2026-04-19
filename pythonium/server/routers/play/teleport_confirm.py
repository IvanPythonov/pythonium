"""Teleport Confirm Router."""

from pythonium.engine.packets.ingoing.play import TeleportConfirm
from pythonium.engine.router import Router

router = Router(name=__name__)


@router.on(TeleportConfirm)
async def teleport_confirm_handler(teleport_confirm: TeleportConfirm) -> None:
    pass
