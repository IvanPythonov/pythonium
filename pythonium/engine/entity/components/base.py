from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pythonium.engine.entity.base import Entity


class Component(ABC):
    """Component."""

    def on_attach(self, entity: "Entity") -> None:
        """On attach."""
        self.entity = entity

    @abstractmethod
    def tick(self, current_tick: int) -> None:
        """Tick logic."""
