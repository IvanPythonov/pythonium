from msgspec import Struct

from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import (
    StringCodec,
    TextComponentCodec,
    UUIDCodec,
    VarIntCodec,
)
from pythonium.engine.codecs.optional import OptionalCodec
from pythonium.engine.codecs.primitives import (
    BooleanCodec,
    ByteCodec,
    LongCodec,
)
from pythonium.engine.exceptions import EncodeError
from pythonium.engine.typealiases import Deserialized


class GameProfilePropertyStruct(Struct):
    """Game profile property struct."""

    name: str
    value: str
    signature: str | None = None


class ChatSignatureDataStruct(Struct):
    """Chat signature data struct."""

    chat_session_id: str  # UUID
    public_key_expiry: int  # Long
    encoded_public_key: bytes  # Byte Array (512)
    public_key_signature: bytes  # Byte Array (4096)


class PlayerInfoActionStruct(Struct):
    """Player info action struct."""

    uuid: str
    # 0x01 - Add Player
    name: str | None = None
    properties: list[GameProfilePropertyStruct] | None = None
    # 0x02 - Initialize Chat
    chat_signature_data: ChatSignatureDataStruct | None = None
    # 0x04 - Update Game Mode
    game_mode: int | None = None
    # 0x08 - Update Listed
    listed: bool | None = None
    # 0x10 - Update Latency
    ping: int | None = None
    # 0x20 - Update Display Name
    display_name: dict | None = None
    # 0x40 - Update List Priority
    list_priority: int | None = None
    # 0x80 - Update Hat
    hat_visible: bool | None = None


class GameProfilePropertyCodec(Codec[GameProfilePropertyStruct]):
    """Game profile property codec."""

    def __init__(self) -> None:
        self.string = StringCodec()
        self.opt_string = OptionalCodec(self.string)

    def serialize(self, *, field: GameProfilePropertyStruct) -> bytes:
        return (
            self.string.serialize(field=field.name)
            + self.string.serialize(field=field.value)
            + self.opt_string.serialize(field=field.signature)
        )

    def deserialize(
        self, data: bytes
    ) -> Deserialized[GameProfilePropertyStruct]:
        name, c1 = self.string.deserialize(data)
        val, c2 = self.string.deserialize(data[c1:])
        sig, c3 = self.opt_string.deserialize(data[c1 + c2 :])
        return GameProfilePropertyStruct(name, val, sig), c1 + c2 + c3


class ChatSignatureDataCodec(Codec[ChatSignatureDataStruct]):
    """Chat signature data codec."""

    def __init__(self) -> None:
        self.uuid = UUIDCodec()
        self.long = LongCodec()
        self.key_bytes: ArrayCodec = ArrayCodec(ByteCodec())
        self.sig_bytes: ArrayCodec = ArrayCodec(ByteCodec())

    def serialize(self, *, field: ChatSignatureDataStruct) -> bytes:
        return (
            self.uuid.serialize(field=field.chat_session_id)
            + self.long.serialize(field=field.public_key_expiry)
            + self.key_bytes.serialize(field=list(field.encoded_public_key))
            + self.sig_bytes.serialize(field=list(field.public_key_signature))
        )

    def deserialize(
        self, data: bytes
    ) -> Deserialized[ChatSignatureDataStruct]:
        sess_id, c1 = self.uuid.deserialize(data)
        exp, c2 = self.long.deserialize(data[c1:])
        pub, c3 = self.key_bytes.deserialize(data[c1 + c2 :])
        sig, c4 = self.sig_bytes.deserialize(data[c1 + c2 + c3 :])
        return ChatSignatureDataStruct(
            sess_id, exp, bytes(pub), bytes(sig)
        ), c1 + c2 + c3 + c4


class PlayerInfoUpdateStruct(Struct):
    """Player info update struct."""

    actions_mask: int  # EnumSet (Bitmask) sent as a Byte
    players: list[PlayerInfoActionStruct]


class PlayerInfoUpdateCodec(Codec[PlayerInfoUpdateStruct]):
    """Codec for Player Info Update."""

    def __init__(self) -> None:
        self.byte = ByteCodec()
        self.varint = VarIntCodec()
        self.uuid = UUIDCodec()
        self.string = StringCodec()
        self.boolean = BooleanCodec()
        self.opt_text = OptionalCodec(TextComponentCodec())
        self.opt_sig_data = OptionalCodec(ChatSignatureDataCodec())
        self.props_array: ArrayCodec = ArrayCodec(GameProfilePropertyCodec())

    def _serialize_player(self, p: PlayerInfoActionStruct, mask: int) -> bytes:
        out = bytearray(self.uuid.serialize(field=p.uuid))

        if mask & 0x01:
            if not p.name or p.properties is None:
                raise EncodeError(info="Add Player requires name & properties")
            out.extend(self.string.serialize(field=p.name))
            out.extend(self.props_array.serialize(field=p.properties))

        if mask & 0x02:
            out.extend(
                self.opt_sig_data.serialize(field=p.chat_signature_data)
            )

        if mask & 0x04:
            if p.game_mode is None:
                raise EncodeError(info="Update GameMode requires game_mode")
            out.extend(self.varint.serialize(field=p.game_mode))

        if mask & 0x08:
            if p.listed is None:
                raise EncodeError(info="Update Listed requires listed")
            out.extend(self.boolean.serialize(field=p.listed))

        if mask & 0x10:
            if p.ping is None:
                raise EncodeError(info="Update Ping requires ping")
            out.extend(self.varint.serialize(field=p.ping))

        if mask & 0x20:
            out.extend(self.opt_text.serialize(field=p.display_name))

        if mask & 0x40:
            if p.list_priority is None:
                raise EncodeError(info="Priority requires list_priority")
            out.extend(self.varint.serialize(field=p.list_priority))

        if mask & 0x80:
            if p.hat_visible is None:
                raise EncodeError(info="Update Hat requires hat_visible")
            out.extend(self.boolean.serialize(field=p.hat_visible))

        return bytes(out)

    def serialize(self, *, field: PlayerInfoUpdateStruct) -> bytes:
        out = bytearray(self.byte.serialize(field=field.actions_mask))
        out.extend(self.varint.serialize(field=len(field.players)))
        for p in field.players:
            out.extend(self._serialize_player(p, field.actions_mask))
        return bytes(out)

    def deserialize(self, data: bytes) -> Deserialized[PlayerInfoUpdateStruct]:
        mask, consumed = self.byte.deserialize(data)
        count, c = self.varint.deserialize(data[consumed:])
        consumed += c

        players = []
        for _ in range(count):
            p_uuid, c = self.uuid.deserialize(data[consumed:])
            consumed += c

            p_action = PlayerInfoActionStruct(uuid=p_uuid)

            if mask & 0x01:
                p_action.name, c = self.string.deserialize(data[consumed:])
                consumed += c
                p_action.properties, c = self.props_array.deserialize(
                    data[consumed:]
                )
                consumed += c

            if mask & 0x02:
                p_action.chat_signature_data, c = (
                    self.opt_sig_data.deserialize(data[consumed:])
                )
                consumed += c

            if mask & 0x04:
                p_action.game_mode, c = self.varint.deserialize(
                    data[consumed:]
                )
                consumed += c

            if mask & 0x08:
                p_action.listed, c = self.boolean.deserialize(data[consumed:])
                consumed += c

            if mask & 0x10:
                p_action.ping, c = self.varint.deserialize(data[consumed:])
                consumed += c

            if mask & 0x20:
                p_action.display_name, c = self.opt_text.deserialize(
                    data[consumed:]
                )
                consumed += c

            if mask & 0x40:
                p_action.list_priority, c = self.varint.deserialize(
                    data[consumed:]
                )
                consumed += c

            if mask & 0x80:
                p_action.hat_visible, c = self.boolean.deserialize(
                    data[consumed:]
                )
                consumed += c

            players.append(p_action)

        return PlayerInfoUpdateStruct(
            actions_mask=mask, players=players
        ), consumed
