import struct
from abc import ABC, abstractmethod
from functools import cache
from typing import (
    Annotated,
    TypeAliasType,
    get_args,
    get_origin,
)

from pythonium.engine.typealiases import Deserialized


class Codec[T](ABC):
    """Class representing codec contract."""

    @abstractmethod
    def serialize(self, *, field: T) -> bytes: ...

    @abstractmethod
    def deserialize(self, data: bytes) -> Deserialized[T]: ...


class PrimitiveCodec[T](Codec[T]):
    """Class representing codec for primitive types."""

    __format_character__: str

    _struct: struct.Struct
    _size: int

    def __init_subclass__(cls) -> None:
        cls._struct = struct.Struct(cls.__format_character__)
        cls._size = cls._struct.size

        if not hasattr(cls, "__format_character__"):
            msg = (
                f"{cls.__name__} used PrimitiveCodec"
                ", but doesn't have `__format_character__`."
            )
            raise NotImplementedError(msg)
        return super().__init_subclass__()

    def serialize(self, *, field: T) -> bytes:
        return self._struct.pack(field)

    def deserialize(self, data: bytes) -> Deserialized[T]:
        value: T = self._struct.unpack(data[: self._size])[0]
        return value, self._size


@cache
def resolve_codec(annotation: TypeAliasType) -> Codec:
    annotation = annotation.evaluate_value()

    if get_origin(annotation) is Annotated:
        args = get_args(annotation)

        for arg in args[1:]:
            if isinstance(arg, Codec):
                return arg
    msg = "Wrong annotation."
    raise TypeError(msg)
