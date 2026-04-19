"""Keep Alive Router."""

from pythonium.engine.packets.ingoing.configuration import (
    KeepAlive as ConfigurationKeepAlive,
)
from pythonium.engine.packets.ingoing.play import KeepAlive as PlayKeepAlive
from pythonium.engine.router import Router

router = Router(name=__name__)


@router.on(ConfigurationKeepAlive, PlayKeepAlive)
async def keep_alive_handler(
    keep_alive: ConfigurationKeepAlive | PlayKeepAlive,
) -> None:
    pass
