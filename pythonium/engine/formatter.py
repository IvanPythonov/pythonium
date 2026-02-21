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


def _format_value(value: Any, level: int = 0) -> str:  # noqa: ANN401
    indent = _INDENT_STEP * level
    next_indent = _INDENT_STEP * (level + 1)

    if value is None:
        return f"{Colors.GRAY}None{Colors.RESET}"

    if value is True:
        return f"{Colors.GREEN}True{Colors.RESET}"

    if value is False:
        return f"{Colors.RED}False{Colors.RESET}"

    if isinstance(value, str):
        return f"{Colors.YELLOW}{value!r}{Colors.RESET}"

    if isinstance(value, (int, float)):
        return f"{Colors.CYAN}{value!r}{Colors.RESET}"

    if isinstance(value, bytes):
        if len(value) > 32:
            snippet = repr(value[:32]) + "..."
            return f"{Colors.BLUE}{snippet}{Colors.RESET} {Colors.GRAY}(len={len(value)}){Colors.RESET}"
        return f"{Colors.BLUE}{value!r}{Colors.RESET}"

    if isinstance(value, (dict, Compound)):
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

    if isinstance(value, (list, tuple)):
        if not value:
            return f"{Colors.GRAY}[]{Colors.RESET}"

        if len(value) < 10 and all(
            isinstance(x, (int, float, bool, str, type(None))) for x in value
        ):
            items = ", ".join(_format_value(x, 0) for x in value)
            return f"{Colors.GRAY}[{Colors.RESET} {items} {Colors.GRAY}]{Colors.RESET}"

        lines = [f"{Colors.GRAY}[{Colors.RESET}"]
        for i, item in enumerate(value):
            formatted_v = _format_value(item, level + 1)
            lines.append(f"{next_indent}{formatted_v},")

        lines[-1] = lines[-1].rstrip(",")
        lines.append(f"{indent}{Colors.GRAY}]{Colors.RESET}")
        return "\n".join(lines)

    return repr(value)


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

    if len(lines) > 2:
        lines[-1] = lines[-1].rstrip(",")

    return "\n".join(lines)
