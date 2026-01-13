"""Some logic for router."""

from pythonium.engine import Client, Router
from pythonium.engine.enums import State
from pythonium.engine.packets import Handshake

router = Router(name=__name__)


@router.on(Handshake)
async def on_handshake(handshake: Handshake, client: Client) -> None:
    client.session.state = (
        State.STATUS if handshake.next_state == 1 else State.PLAY
    )
