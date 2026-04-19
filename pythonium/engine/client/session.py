import asyncio
from typing import final

from msgspec import Struct

from pythonium.engine.enums.states import State


@final
class ClientSession(Struct):
    """Class representing Minecraft client session."""

    background_tasks: set[asyncio.Task] = set()

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

    visible_chunks: set[tuple[int, int]] = set()
    last_chunk_center: tuple[int, int] | None = None

    chunk_send_lock = asyncio.Lock()
    chunk_ack_future: asyncio.Future | None = None
