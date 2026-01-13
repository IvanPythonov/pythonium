from pythonium.engine.client.connection import ClientConnection
from pythonium.engine.client.session import ClientSession


class Client:
    """Class representing Minecraft client."""

    def __init__(
        self, connection: ClientConnection, session: ClientSession
    ) -> None:
        self.connection = connection
        self.session = session

        self.unique_id = connection.address
