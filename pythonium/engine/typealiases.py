from collections.abc import Awaitable, Callable, Iterable
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from pythonium.engine.packets.base import Packet

type Consumed = int
type Deserialized[T] = tuple[T, Consumed]

type Handler = Callable[..., Awaitable[None]]
type RegistryHandler = Callable[..., Awaitable[Iterable[Packet] | None]]


class TextComponent(TypedDict):
    """Text component."""

    text: str
