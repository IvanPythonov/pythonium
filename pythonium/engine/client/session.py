import asyncio
from typing import final

from msgspec import Struct

from pythonium.engine.enums.states import State


@final
class ClientSession(Struct):
    """Client session."""

    background_tasks: set[asyncio.Task] = set()

    state: State = State.HANDSHAKING
