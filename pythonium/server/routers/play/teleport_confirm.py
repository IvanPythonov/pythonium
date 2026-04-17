"""Teleport Confirm Router."""

from pythonium.engine.packets.ingoing.play import TeleportConfirm
from pythonium.server.routers.play import router as play_router


@play_router.on(TeleportConfirm)
async def teleport_confirm_handler(teleport_confirm: TeleportConfirm) -> None:
    pass
