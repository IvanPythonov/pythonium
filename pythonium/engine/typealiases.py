from collections.abc import Awaitable, Callable
from typing import TypedDict

type Consumed = int
type Deserialized[T] = tuple[T, Consumed]

type Handler = Callable[..., Awaitable[None]]


class TextComponent(TypedDict):
    """Text component."""

    text: str
