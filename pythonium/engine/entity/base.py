import uuid
from copy import deepcopy
from typing import Any

from pythonium.engine.entity.components.base import Component
from pythonium.engine.entity.tracked_data import TrackedData
from pythonium.engine.packets.outgoing.play import EntityMetadata
from pythonium.engine.ticker.tickable import Tickable


class Entity(Tickable):
    """Entity."""

    entity_type: int = 0

    def __init_subclass__(cls, **kwargs: Any):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "entity_type"):
            msg = f"Class {cls.__name__} must define entity_type"
            raise TypeError(msg)

    def __init__(self, x: float, y: float, z: float) -> None:
        self.entity_id = 0

        self.object_uuid = uuid.uuid4()

        self.x, self.y, self.z = x, y, z
        self.velocity_x = self.velocity_y = self.velocity_z = 0.0

        self.on_ground = True
        self.removed = False

        self.metadata: dict[int, tuple[int, Any]] = {}
        self.dirty_metadata: dict[int, tuple[int, Any]] = {}

        for attr_name in dir(self.__class__):
            attr = getattr(self.__class__, attr_name)
            if isinstance(attr, TrackedData):
                self.metadata[attr.index] = (attr.type_id, attr.default)

        self.components: list[Component] = []
        for attr_name, attr_value in self.__class__.__dict__.items():
            if isinstance(attr_value, Component):
                comp_instance = deepcopy(attr_value)
                comp_instance.on_attach(self)
                self.components.append(comp_instance)
                setattr(self, attr_name, comp_instance)

    def popdirty_metadata(self) -> dict[int, tuple[int, Any]]:
        if not self.dirty_metadata:
            return {}
        dirty = self.dirty_metadata.copy()
        self.dirty_metadata.clear()
        return dirty

    def despawn(self) -> None:
        if self.removed:
            return
        self.removed = True

    def tick(self, current_tick: int) -> None:
        for component in self.components:
            component.tick(current_tick)
