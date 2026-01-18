from typing import TypedDict

type Consumed = int
type Deserialized[T] = tuple[T, Consumed]


class TextComponent(TypedDict):
    """Text component."""

    text: str
