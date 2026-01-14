import struct
from typing import Annotated, ClassVar, get_args, get_origin

from pythonium.engine.typealiases import Deserialized


class Codec[T]:
    """Class representing codec contract."""

    def serialize(self, data: T) -> bytes:
        raise NotImplementedError

    def deserialize(self, data: bytes) -> Deserialized[T]:
        raise NotImplementedError


class ArrayCodec[T](Codec):
    """Codec for arrays prefixed with length."""

    __element_codec__: ClassVar[Codec]
    __length_codec__: ClassVar[Codec | None] = None

    def serialize(self, value: list[T]) -> bytes:
        from pythonium.engine.codecs.custom import VarIntCodec  # noqa: PLC0415

        length_codec = self.__length_codec__ or VarIntCodec()
        length_bytes = length_codec.serialize(len(value))
        element_bytes = b"".join(
            self.__element_codec__.serialize(item) for item in value
        )
        return length_bytes + element_bytes

    def deserialize(self, data: bytes) -> Deserialized[list[T]]:
        from pythonium.engine.codecs.custom import VarIntCodec  # noqa: PLC0415

        length_codec = self.__length_codec__ or VarIntCodec()
        length, offset = length_codec.deserialize(data)
        result = []

        for _ in range(length):
            item, item_size = self.__element_codec__.deserialize(data[offset:])
            result.append(item)
            offset += item_size

        return result, offset


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

    def serialize(self, data: T) -> bytes:
        return struct.pack(self.__format_character__, data)

    def deserialize(self, data: bytes) -> Deserialized[T]:
        size: int = struct.calcsize(self.__format_character__)
        value: T = struct.unpack(self.__format_character__, data[:size])[0]
        return value, size


def resolve_codec(annotation: Annotated[object, Codec()]) -> Codec:
    if get_origin(annotation) is Annotated:
        args = get_args(annotation)

        for arg in args[1:]:
            if isinstance(arg, Codec):
                return arg
    msg = "Wrong annotation."
    raise TypeError(msg)
