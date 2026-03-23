from typing import Final

from msgspec import Struct

from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import (
    FixedByteArrayCodec,
    StringCodec,
    VarIntCodec,
)
from pythonium.engine.exceptions import DecodeError, EncodeError
from pythonium.engine.typealiases import Deserialized

SIGNATURE_SIZE: Final[int] = 256


class MessageSignatureStruct(Struct):
    """Struct representing Message Signature."""

    message_id: int
    signature: bytes | None = None


class MessageSignatureCodec(Codec[MessageSignatureStruct]):
    """
    Codec for Message Signatures.

    If Message ID is 0, a 256-byte signature follows (no length prefix).
    If Message ID > 0, there is no signature.
    """

    def __init__(self) -> None:
        self.varint = VarIntCodec()

    def serialize(self, *, field: MessageSignatureStruct) -> bytes:
        data = bytearray(self.varint.serialize(field=field.message_id))

        if field.message_id == 0:
            if not field.signature or len(field.signature) != SIGNATURE_SIZE:
                raise EncodeError(
                    info=(
                        f"Signature must be exactly {SIGNATURE_SIZE} bytes "
                        "when message_id is 0."
                    ),
                )
            data.extend(field.signature)

        return bytes(data)

    def deserialize(self, data: bytes) -> Deserialized[MessageSignatureStruct]:
        message_id, consumed = self.varint.deserialize(data)

        signature = None
        if message_id == 0:
            if len(data) - consumed < SIGNATURE_SIZE:
                raise DecodeError(
                    info=(
                        f"Not enough bytes for {SIGNATURE_SIZE}-byte"
                        "message signature."
                    ),
                    available=len(data) - consumed,
                )
            signature = data[consumed : consumed + SIGNATURE_SIZE]
            consumed += SIGNATURE_SIZE

        return MessageSignatureStruct(
            message_id=message_id, signature=signature
        ), consumed


class ArgumentSignatureStruct(Struct):
    """Argument signature struct."""

    argument_name: str
    signature: bytes


class ArgumentSignatureCodec(Codec[ArgumentSignatureStruct]):
    """Argument signature codec."""

    def __init__(self) -> None:
        self.string = StringCodec()
        self.signature = FixedByteArrayCodec(256)

    def serialize(self, *, field: ArgumentSignatureStruct) -> bytes:
        return self.string.serialize(
            field=field.argument_name
        ) + self.signature.serialize(field=field.signature)

    def deserialize(
        self, data: bytes
    ) -> Deserialized[ArgumentSignatureStruct]:
        name, c1 = self.string.deserialize(data)
        sig, c2 = self.signature.deserialize(data[c1:])
        return ArgumentSignatureStruct(name, sig), c1 + c2
