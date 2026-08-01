from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pythonium.engine.entity.base import Entity


class TrackedData[T]:
    """Aidsaodiuaspo."""

    def __init__(self, index: int, type_id: int, default: T) -> None:
        self.index = index
        self.type_id = type_id
        self.default = default
        self.name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: "Entity", owner: type) -> T:
        if instance is None:
            return self
        return instance.metadata.get(self.index, (self.type_id, self.default))[
            1
        ]

    def __set__(self, instance: "Entity", value: T) -> None:
        current_value = instance.metadata.get(
            self.index, (self.type_id, self.default)
        )[1]
        if current_value != value:
            instance.metadata[self.index] = (self.type_id, value)
            instance.dirty_metadata[self.index] = (self.type_id, value)
