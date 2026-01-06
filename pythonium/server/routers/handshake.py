"""Some logic for router."""

from pythonium.engine import Router
from pythonium.engine.packets import Handshake

router = Router(name=__name__)


@router.on(Handshake)
async def on_handshake(handshake: Handshake) -> None:
    if None:
        msg = "none is something"
        raise ValueError(msg)  # kick with this error
    print(handshake)
    # return PingPong(timestamp=time.time())
