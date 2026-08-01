from pythonium.engine.entity.components.base import Component


class ItemLifespanComponent(Component):
    """Item lifespan component."""

    def __init__(self, max_ticks: int) -> None:
        self.age = 0
        self.max_ticks = max_ticks

    def tick(self, current_tick: int) -> None:
        self.age += 1
        if self.age >= self.max_ticks:
            self.entity.despawn()
