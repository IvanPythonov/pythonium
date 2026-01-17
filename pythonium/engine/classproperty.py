from collections.abc import Callable
from typing import overload


class ClassProperty[T]:
    """Descriptor for class-level properties."""

    def __init__(self, function: Callable[[type], T]) -> None:
        self.function = function

    @overload
    def __get__(self, _object: None, owner: type) -> T: ...

    @overload
    def __get__(self, _object: object, owner: type) -> T: ...

    def __get__(self, _object: object | None, owner: type) -> T:
        return self.function(owner)
