from msgspec import Struct


class PlayerSession(Struct):
    """Player session."""

    uuid: str
    username: str

    game_mode: int = 1

    view_distance: int = 10

    locale: str | None = None
    chat_mode: int | None = None
    chat_colors: int | None = None
    enable_text_filtering: bool | None = None
    allow_server_listings: bool | None = None
    particle_status: int | None = None

    displayed_skin_parts: int | None = None
    main_hand: int | None = None

    loaded_chunks: set[tuple[int, int]] = set()
    last_chunk_center: tuple[int, int] | None = None
