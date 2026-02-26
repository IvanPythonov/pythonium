from typing import Protocol


class Tickable(Protocol):
    """Class representing tickable protocol."""

    def tick(self, current_tick: int) -> None: ...
