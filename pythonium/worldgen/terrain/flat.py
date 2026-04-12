from pythonium.worldgen.base import IWorldGenerator


class FlatWorldGenerator(IWorldGenerator):
    """Flat world generator."""

    def generate_chunk(self, x: int, z: int) -> bytes:
        """Generate chunk data for given coordinates."""
