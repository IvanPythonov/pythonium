from asyncio import StreamReader, StreamWriter

from pythonium.engine import Client
from pythonium.engine.client import ClientConnection, ClientSession
from pythonium.engine.enums import State


def build_client(
    reader: StreamReader,
    writer: StreamWriter,
) -> Client:
    return Client(
        connection=ClientConnection(reader, writer),
        session=ClientSession(state=State.HANDSHAKING),
    )
