from typing import Protocol


class IWorldGenerator(Protocol):
    """Interface for world generator."""

    def generate_chunk(self, x: int, z: int) -> bytes:
        """Generate chunk data for given coordinates."""
