from msgspec import Struct

from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import StringCodec, VarIntCodec
from pythonium.engine.codecs.nbt import NBTCodec
from pythonium.engine.exceptions import EncodeError
from pythonium.engine.typealiases import Deserialized


class ChatTypeDecorationStruct(Struct):
    """Struct for Chat Type Decoration."""

    translation_key: str
    parameters: list[
        int
    ]  # Array of VarInt Enum (0: sender, 1: target, 2: content)
    # TODO(IvanPythonov): enums
    style: dict  # NBT Compound


class ChatTypeDecorationCodec(Codec[ChatTypeDecorationStruct]):
    """Codec for Chat Type Decoration."""

    def __init__(self) -> None:
        self.string = StringCodec()
        self.varint_array: ArrayCodec = ArrayCodec(VarIntCodec())
        self.nbt = NBTCodec()

    def serialize(self, *, field: ChatTypeDecorationStruct) -> bytes:
        return b"".join(
            [
                self.string.serialize(field=field.translation_key),
                self.varint_array.serialize(field=field.parameters),
                self.nbt.serialize(field=field.style),
            ]
        )

    def deserialize(
        self, data: bytes
    ) -> Deserialized[ChatTypeDecorationStruct]:
        t_key, c1 = self.string.deserialize(data)
        params, c2 = self.varint_array.deserialize(data[c1:])
        style, c3 = self.nbt.deserialize(data[c1 + c2 :])
        return ChatTypeDecorationStruct(t_key, params, style), c1 + c2 + c3


class InlineChatTypeStruct(Struct):
    """Struct for Inline Chat Type definition."""

    chat: ChatTypeDecorationStruct
    narration: ChatTypeDecorationStruct


class ChatTypeStruct(Struct):
    """Struct for ID or Chat Type."""

    registry_id: int
    inline_data: InlineChatTypeStruct | None = None


class ChatTypeCodec(Codec[ChatTypeStruct]):
    """Codec for 'ID or Chat Type' polymorphic field."""

    def __init__(self) -> None:
        self.varint = VarIntCodec()
        self.decoration = ChatTypeDecorationCodec()

    def serialize(self, *, field: ChatTypeStruct) -> bytes:
        out = bytearray(self.varint.serialize(field=field.registry_id))

        if field.registry_id == 0:
            if field.inline_data is None:
                raise EncodeError(
                    info="inline_data is required if registry_id is 0"
                )

            out.extend(self.decoration.serialize(field=field.inline_data.chat))
            out.extend(
                self.decoration.serialize(field=field.inline_data.narration)
            )

        return bytes(out)

    def deserialize(self, data: bytes) -> Deserialized[ChatTypeStruct]:
        reg_id, consumed = self.varint.deserialize(data)
        inline_data = None

        if reg_id == 0:
            chat_dec, c1 = self.decoration.deserialize(data[consumed:])
            narration_dec, c2 = self.decoration.deserialize(
                data[consumed + c1 :]
            )
            consumed += c1 + c2
            inline_data = InlineChatTypeStruct(
                chat=chat_dec, narration=narration_dec
            )

        return ChatTypeStruct(
            registry_id=reg_id, inline_data=inline_data
        ), consumed
