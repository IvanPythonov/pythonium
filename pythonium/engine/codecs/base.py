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

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "__format_character__"):
            msg = (
                f"{cls.__name__} used PrimitiveCodec"
                ", but doesn't have `__format_character__`."
            )
            raise NotImplementedError(msg)
        return super().__init_subclass__()

    def serialize(self, *, field: T) -> bytes:
        return struct.pack(self.__format_character__, field)

    def deserialize(self, data: bytes) -> Deserialized[T]:
        size: int = struct.calcsize(self.__format_character__)
        value: T = struct.unpack(self.__format_character__, data[:size])[0]
        return value, size


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
