"""Handshake Phase Router."""

from pythonium.engine import Client, Router
from pythonium.engine.enums import NextState
from pythonium.engine.packets.ingoing import SetProtocol

router = Router(name=__name__)


@router.on(SetProtocol)
async def on_handshake(handshake: SetProtocol, client: Client) -> None:
    client.session.state = NextState(handshake.next_state)
