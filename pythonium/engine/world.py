from typing import Self

from pythonium.engine.ticker.tickable import Tickable


class World:
    """Class representing game world."""

    def __init__(self) -> None:
        self.entities: set[Tickable] = set()
        self.blocks_to_tick: list[Tickable] = []

    def add_entity(self, entity: Tickable) -> Self:
        self.entities.add(entity)
        return self

    def remove_entity(self, entity: Tickable) -> Self:
        self.entities.discard(entity)
        return self

    def tick(self, current_tick: int) -> None:
        for entity in self.entities:
            entity.tick(current_tick)
