from typing import final

from msgspec import Struct

from pythonium.engine.enums import State


@final
class ClientSession(Struct, slots=True):
    """Class representing Minecraft client session."""

    state: State = State.HANDSHAKING
