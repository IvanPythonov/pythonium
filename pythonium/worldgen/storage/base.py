from typing import Protocol


class IStorage(Protocol):
    """Interface for storage."""

    def save_chunk(self, x: int, z: int, data: bytes) -> None:
        """Save chunk data for given coordinates."""

    def load_chunk(self, x: int, z: int) -> bytes | None:
        """Load chunk data for given coordinates."""
