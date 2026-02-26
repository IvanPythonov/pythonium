from enum import StrEnum
from typing import TYPE_CHECKING, Any

try:
    from nbtlib import Compound
except ImportError:
    from collections import UserDict as Compound  # Fallback for type checking

from pythonium.engine.codecs import Codec, OptionalCodec

if TYPE_CHECKING:
    from pythonium.engine.packets.base import Packet

_INDENT_STEP = "    "
_BYTES_TRUNCATE_LENGTH = 32
_SIMPLE_LIST_MAX_LENGTH = 10
_MIN_LINES_FOR_COMMA_STRIP = 2


class Colors(StrEnum):
    """Colors enumeration."""

    GREEN_BOLD = "\033[1;32m"
    GRAY = "\033[90m"
    CYAN_BRIGHT = "\033[96m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[36m"
    PURPLE = "\033[35m"
    BLUE = "\033[34m"
    RESET = "\033[0m"


def _get_codec_name(codec: Codec[Any]) -> str:
    match codec:
        case OptionalCodec():
            return f"Optional[{_get_codec_name(codec.inner_codec)}]"
        case _:
            return codec.__class__.__name__.removesuffix("Codec")


def _format_none() -> str:
    return f"{Colors.GRAY}None{Colors.RESET}"


def _format_bool(value: bool) -> str:  # noqa: FBT001
    color = Colors.GREEN if value else Colors.RED
    return f"{color}{value}{Colors.RESET}"


def _format_string(value: str) -> str:
    return f"{Colors.YELLOW}{value!r}{Colors.RESET}"


def _format_number(value: float) -> str:
    return f"{Colors.CYAN}{value!r}{Colors.RESET}"


def _format_bytes(value: bytes) -> str:
    if len(value) > _BYTES_TRUNCATE_LENGTH:
        snippet = repr(value[:_BYTES_TRUNCATE_LENGTH]) + "..."
        length_info = f"{Colors.GRAY}(len={len(value)}){Colors.RESET}"
        return f"{Colors.BLUE}{snippet}{Colors.RESET} {length_info}"
    return f"{Colors.BLUE}{value!r}{Colors.RESET}"


def _format_dict(value: dict | Compound, level: int) -> str:
    indent = _INDENT_STEP * level
    next_indent = _INDENT_STEP * (level + 1)

    if not value:
        return f"{Colors.GRAY}{{}}{Colors.RESET}"

    lines = [f"{Colors.GRAY}{{{Colors.RESET}"]
    for k, v in value.items():
        formatted_k = f"{Colors.PURPLE}{k!r}{Colors.RESET}"
        formatted_v = _format_value(v, level + 1)
        lines.append(f"{next_indent}{formatted_k}: {formatted_v},")

    lines[-1] = lines[-1].rstrip(",")
    lines.append(f"{indent}{Colors.GRAY}}}{Colors.RESET}")
    return "\n".join(lines)


def _format_sequence(value: list | tuple, level: int) -> str:
    indent = _INDENT_STEP * level
    next_indent = _INDENT_STEP * (level + 1)

    if not value:
        return f"{Colors.GRAY}[]{Colors.RESET}"

    if len(value) < _SIMPLE_LIST_MAX_LENGTH and all(
        isinstance(x, (int, float, bool, str, type(None))) for x in value
    ):
        items = ", ".join(_format_value(x, 0) for x in value)
        return (
            f"{Colors.GRAY}[{Colors.RESET} "
            f"{items} "
            f"{Colors.GRAY}]{Colors.RESET}"
        )

    lines = [f"{Colors.GRAY}[{Colors.RESET}"]
    for _, item in enumerate(value):
        formatted_v = _format_value(item, level + 1)
        lines.append(f"{next_indent}{formatted_v},")

    lines[-1] = lines[-1].rstrip(",")
    lines.append(f"{indent}{Colors.GRAY}]{Colors.RESET}")
    return "\n".join(lines)


def _format_value(value: Any, level: int = 0) -> str:  # noqa: ANN401
    result: str

    if value is None:
        result = _format_none()
    elif isinstance(value, bool):
        result = _format_bool(value)
    elif isinstance(value, str):
        result = _format_string(value)
    elif isinstance(value, (int, float)):
        result = _format_number(value)
    elif isinstance(value, bytes):
        result = _format_bytes(value)
    elif isinstance(value, (dict, Compound)):
        result = _format_dict(value, level)
    elif isinstance(value, (list, tuple)):
        result = _format_sequence(value, level)
    else:
        result = repr(value)

    return result


def _format_field(name: str, value: Any, codec: Codec[Any]) -> str:  # noqa: ANN401
    codec_name = _get_codec_name(codec)
    formatted_value = _format_value(value, level=1)

    return (
        f"{_INDENT_STEP}{Colors.GRAY}({codec_name}){Colors.RESET} "
        f"{Colors.CYAN_BRIGHT}{name}{Colors.RESET}: {formatted_value}"
    )


def format_packet(packet: "Packet") -> str:
    lines: list[str] = [
        f"\n{Colors.GREEN_BOLD}({packet.__class__.__name__}):{Colors.RESET}"
    ]

    packet_id_value = f"{Colors.CYAN}{packet.packet_id:#04x}{Colors.RESET}"
    lines.append(
        f"{_INDENT_STEP}{Colors.GRAY}(VarInt){Colors.RESET} "
        f"{Colors.CYAN_BRIGHT}packet_id{Colors.RESET}: {packet_id_value},"
    )
    schema = packet.get_schema()

    for field in schema:
        value = getattr(packet, field.name)
        lines.append(_format_field(field.name, value, field.codec) + ",")

    if len(lines) > _MIN_LINES_FOR_COMMA_STRIP:
        lines[-1] = lines[-1].rstrip(",")

    return "\n".join(lines)
