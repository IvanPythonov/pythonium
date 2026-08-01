import random

from pythonium.engine.codecs.slot import SlotStruct
from pythonium.engine.entity.base import Entity
from pythonium.engine.entity.components.gravity import GravityComponent
from pythonium.engine.entity.components.lifespan import ItemLifespanComponent
from pythonium.engine.entity.tracked_data import TrackedData


class ItemEntity(Entity):
    """Item entity."""

    entity_type = 69

    shared_flags = TrackedData[int](index=0, type_id=0, default=0)
    air_supply = TrackedData[int](index=1, type_id=1, default=300)
    custom_name = TrackedData[dict | None](index=2, type_id=6, default=None)
    custom_name_visible = TrackedData[bool](index=3, type_id=8, default=False)
    silent = TrackedData[bool](index=4, type_id=8, default=False)
    no_gravity = TrackedData[bool](index=5, type_id=8, default=False)
    pose = TrackedData[int](index=6, type_id=21, default=0)
    ticks_frozen = TrackedData[int](index=7, type_id=1, default=0)

    item_slot = TrackedData[SlotStruct](
        index=8, type_id=7, default=SlotStruct(item_count=1, item_id=1)
    )

    gravity = GravityComponent()
    lifespan = ItemLifespanComponent(max_ticks=6_000)

    def __init__(
        self, x: float, y: float, z: float, item_id: int, count: int = 1
    ) -> None:
        super().__init__(x, y, z)
        self.item_slot = SlotStruct(item_count=count, item_id=item_id)

        self.velocity_x = random.SystemRandom().uniform(-0.1, 0.1)
        self.velocity_y = 0.2
        self.velocity_z = random.SystemRandom().uniform(-0.1, 0.1)
