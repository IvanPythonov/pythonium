from pathlib import Path
from typing import Self


class Registry[T]:
    """Base registry."""

    __registry_path__: Path | str

    def __init__(self) -> None:
        self._items: dict[str, T] = {}

    def __init_subclass__(cls) -> None:
        required_attributes = ("__registry_path__", "discover")
        for attr in required_attributes:
            if not hasattr(cls, attr):
                msg = (
                    f"{cls.__name__} used Registry, but doesn't have `{attr}`."
                )
                raise NotImplementedError(msg)
        return super().__init_subclass__()

    def register(self, key: str, item: T) -> Self:
        self._items[key] = item
        return self

    def get(self, key: str) -> list[T]:
        return self._items[key]

    def keys(self) -> list[str]:
        return list(self._items.keys())

    def values(self) -> list[T]:
        return list(self._items.values())

    def __contains__(self, key: str) -> bool:
        return key in self._items
