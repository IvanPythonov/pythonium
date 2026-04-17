from typing import final

from msgspec import Struct

from pythonium.engine.enums import State


@final
class ClientSession(Struct):
    """Class representing Minecraft client session."""

    state: State = State.HANDSHAKING

    uuid: str | None = None
    username: str | None = None

    locale: str | None = None
    chat_mode: int | None = None
    chat_colors: bool | None = None

    enable_text_filtering: bool | None = None
    allow_server_listings: bool | None = None

    particle_status: int | None = None

    # TODO @IvanPythonov: realize player class

    view_distance: int | None = None

    displayed_skin_parts: int | None = None
    main_hand: int | None = None
