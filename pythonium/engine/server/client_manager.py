from collections.abc import Iterator
from typing import Self

from pythonium.engine import Client


class ClientManager:
    """Client manager."""

    def __init__(self) -> None:
        self._clients: set[Client] = set()

    def add(self, client: Client) -> Self:
        self._clients.add(client)
        return self

    def remove(self, client: Client) -> Self:
        self._clients.remove(client)
        return self

    def __iter__(self) -> Iterator[Client]:
        return iter(self._clients)

    def __len__(self) -> int:
        return len(self._clients)

    def __contains__(self, client: Client) -> bool:
        return client in self._clients
