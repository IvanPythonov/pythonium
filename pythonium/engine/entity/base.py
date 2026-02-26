from pythonium.engine.enums.dimensions import Dimension
from pythonium.engine.snapshots.entity import EntitySnapshot
from pythonium.engine.types import Int, NBTCompound, Position


class Entity:
    """Base class for an entity."""

    __snapshot__: EntitySnapshot

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "__snapshot__"):
            msg = f"{cls.__name__} must define `snapshot`"
            raise NotImplementedError(msg)

    def __init__(
        self,
        entity_id: Int,
        position_data: tuple[Position, Position, Dimension],
        rotation: tuple[Int, Int] = (0, 0),
        nbt_tags: NBTCompound | None = None,
    ) -> None:
        if nbt_tags is None:
            nbt_tags = {}

        entity_location, velocity, dimension = position_data

        self.entity_id = entity_id
        self.dimension = dimension
        self.x_rotation = rotation[0]
        self.y_rotation = rotation[1]
        self.velocity: Position = velocity
        self.entity_location: Position = entity_location
        self.nbt_tags: NBTCompound | None = nbt_tags

    def move(
        self,
        entity_location: Position,
        x_rot: Int | None = None,
        y_rot: Int | None = None,
    ) -> None:
        self.entity_location = entity_location
        if x_rot is not None:
            self.x_rotation = x_rot
        if y_rot is not None:
            self.y_rotation = y_rot

    def snapshot(self) -> EntitySnapshot:
        return EntitySnapshot(
            entity_id=self.entity_id,
            x=self.entity_location,
            velocity=self.velocity,
            x_rotation=self.x_rotation,
            y_rotation=self.y_rotation,
            dimension=self.dimension,
            nbt_tags=self.nbt_tags,
        )

    def tick(self, _current_tick: int) -> None:
        return
