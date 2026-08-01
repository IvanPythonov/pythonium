from typing import TYPE_CHECKING

from pythonium.engine.player.session import PlayerSession

if TYPE_CHECKING:
    from pythonium.engine import Client


class Player:
    """Player."""

    def __init__(self, uuid: str, username: str, client: Client) -> None:
        self.uuid = uuid
        self.username = username
        self.client = client

        self.session = PlayerSession(uuid=uuid, username=username)
