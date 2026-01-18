from msgspec import Struct

from pythonium.engine.enums.dimensions import Dimension
from pythonium.engine.types import Int, Position


class EntitySnapshot(Struct, kw_only=True):
    """Snapshot of entity."""

    entity_id: Int
    x: Position
    velocity: Position
    x_rotation: Int
    y_rotation: Int
    dimension: Dimension
    nbt_tags: dict
