from msgspec import Struct

from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.base import Codec
from pythonium.engine.codecs.custom import StringCodec, VarIntCodec
from pythonium.engine.codecs.primitives import ByteCodec
from pythonium.engine.exceptions import DecodeError, EncodeError
from pythonium.engine.typealiases import Deserialized

NODE_TYPE_ROOT = 0
NODE_TYPE_LITERAL = 1
NODE_TYPE_ARGUMENT = 2


class NodeStruct(Struct):
    """Struct representing a command graph node."""

    flags: int
    children: list[int]
    redirect_node: int | None = None
    name: str | None = None
    parser_id: int | None = None
    properties: bytes | None = None
    suggestions_type: str | None = None


class NodeCodec(Codec[NodeStruct]):
    """Codec for command graph nodes."""

    def __init__(self) -> None:
        self.byte = ByteCodec()
        self.varint = VarIntCodec()
        self.string = StringCodec()
        self.varint_array: ArrayCodec = ArrayCodec(self.varint)

    def serialize(self, *, field: NodeStruct) -> bytes:
        out = bytearray(self.byte.serialize(field=field.flags))
        out.extend(self.varint_array.serialize(field=field.children))

        if field.flags & 0x08:
            if field.redirect_node is None:
                raise EncodeError(
                    info="redirect_node is required when flag 0x08 is set"
                )
            out.extend(self.varint.serialize(field=field.redirect_node))

        node_type = field.flags & 0x03
        if node_type in (NODE_TYPE_LITERAL, NODE_TYPE_ARGUMENT):
            if field.name is None:
                raise EncodeError(
                    info="name is required for literal and argument nodes"
                )
            out.extend(self.string.serialize(field=field.name))

        if node_type == NODE_TYPE_ARGUMENT:
            if field.parser_id is None:
                raise EncodeError(
                    info="parser_id is required for argument nodes"
                )
            out.extend(self.varint.serialize(field=field.parser_id))

            if field.properties:
                out.extend(field.properties)

            if field.flags & 0x10:
                if field.suggestions_type is None:
                    raise EncodeError(
                        info=(
                            "suggestions_type is required "
                            "when flag 0x10 is set"
                        )
                    )
                out.extend(self.string.serialize(field=field.suggestions_type))

        return bytes(out)

    def deserialize(self, data: bytes) -> Deserialized[NodeStruct]:  # noqa: ARG002
        raise DecodeError(
            reason=(
                "Deserialization of argument node properties is not supported "
                "without a parser ID mapping. DeclareCommands is clientbound."
            )
        )


class CommandGraphStruct(Struct):
    """Struct representing the full command graph."""

    nodes: list[NodeStruct]
    root_index: int


class CommandGraphCodec(Codec[CommandGraphStruct]):
    """Codec for the full command graph."""

    def __init__(self) -> None:
        self.node_array: ArrayCodec = ArrayCodec(NodeCodec())
        self.varint = VarIntCodec()

    def serialize(self, *, field: CommandGraphStruct) -> bytes:
        return self.node_array.serialize(
            field=field.nodes
        ) + self.varint.serialize(field=field.root_index)

    def deserialize(self, data: bytes) -> Deserialized[CommandGraphStruct]:
        nodes, c1 = self.node_array.deserialize(data)
        root_index, c2 = self.varint.deserialize(data[c1:])
        return CommandGraphStruct(nodes=nodes, root_index=root_index), c1 + c2
