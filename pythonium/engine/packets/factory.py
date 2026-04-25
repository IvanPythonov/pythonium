import ast
import struct
import typing
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Protocol

from pythonium.engine.codecs.base import PrimitiveCodec
from pythonium.engine.codecs.custom import VarIntCodec
from pythonium.engine.field import Field

if TYPE_CHECKING:
    from pythonium.engine.packets.base import Packet


'''
class SetDifficulty(Packet, kw_only=True):
    """Packet representing SetDifficulty."""

    __packet_name__: ClassVar[str] = "play:serverbound:set_difficulty"

    new_difficulty: Difficulty
'''


def flush_primitives(
    current_formats: list[str],
    final_elements: list[ast.Call],
    current_fields: list[ast.Attribute],
) -> None:
    if not current_formats:
        return

    fmt_str = ">" + "".join(current_formats)

    pack_call = ast.Call(
        func=ast.Attribute(
            value=ast.Name(id="struct", ctx=ast.Load()),
            attr="pack",
            ctx=ast.Load(),
        ),
        args=[ast.Constant(value=fmt_str), *current_fields],
    )

    final_elements.append(pack_call)

    current_formats.clear()
    current_fields.clear()


class SerializeFactory[P: "Packet"](Protocol):
    """Class representing serialize factory."""

    @staticmethod
    def get(fields: list[Field]) -> Callable[[P], bytes]:
        current_formats: list[str] = []
        current_fields: list[ast.Attribute] = []
        final_elements: list[ast.Call] = [
            ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="_packet_id_codec", ctx=ast.Load()),
                    attr="serialize",
                    ctx=ast.Load(),
                ),
                keywords=[
                    ast.keyword(
                        arg="field",
                        value=ast.Attribute(
                            value=ast.Name(id="self", ctx=ast.Load()),
                            attr="packet_id",
                            ctx=ast.Load(),
                        ),
                    )
                ],
            )
        ]

        exec_locals: dict[str, Any] = {}
        dynamic_namespace: dict[str, Any] = {"_packet_id_codec": VarIntCodec()}

        for field in fields:
            codec = field.codec

            if isinstance(codec, PrimitiveCodec):
                dynamic_namespace["struct"] = struct

                current_formats.append(
                    codec.__format_character__.replace(">", "")
                )
                current_fields.append(
                    ast.Attribute(
                        value=ast.Name(id="self", ctx=ast.Load()),
                        attr=field.name,
                        ctx=ast.Load(),
                    )
                )
            else:
                flush_primitives(
                    current_fields=current_fields,
                    current_formats=current_formats,
                    final_elements=final_elements,
                )

                codec_name = f"_{field.name}_codec"
                dynamic_namespace[codec_name] = codec

                complex_call = ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id=codec_name, ctx=ast.Load()),
                        attr="serialize",
                        ctx=ast.Load(),
                    ),
                    keywords=[
                        ast.keyword(
                            arg="field",
                            value=ast.Attribute(
                                value=ast.Name(id="self", ctx=ast.Load()),
                                attr=field.name,
                                ctx=ast.Load(),
                            ),
                        )
                    ],
                )

                final_elements.append(complex_call)
        flush_primitives(
            current_fields=current_fields,
            current_formats=current_formats,
            final_elements=final_elements,
        )

        serialize_ast = ast.Module(
            body=[
                ast.FunctionDef(
                    name="serialize",
                    args=ast.arguments(args=[ast.arg(arg="self")]),
                    body=[
                        ast.Return(
                            value=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Constant(value=b""),
                                    attr="join",
                                    ctx=ast.Load(),
                                ),
                                args=[
                                    ast.List(
                                        elts=typing.cast(
                                            "list[ast.expr]", final_elements
                                        ),
                                        ctx=ast.Load(),
                                    )
                                ],
                            )
                        )
                    ],
                )
            ]
        )

        ast.fix_missing_locations(serialize_ast)

        exec(  # noqa: S102
            compile(source=serialize_ast, filename="<ast>", mode="exec"),
            globals=dynamic_namespace,
            locals=exec_locals,
        )
        return exec_locals["serialize"]
