from enum import Enum, StrEnum
from typing import TYPE_CHECKING, Any

from msgspec import Struct
from msgspec.structs import fields as get_struct_fields

if TYPE_CHECKING:
    from pythonium.engine.packets.base import Packet


class Colors(StrEnum):
    """Colors string enum."""

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


_INDENT = "    "


def _format_value(value: Any, level: int = 0) -> str:  # noqa: ANN401, C901, PLR0911
    if value is None:
        return f"{Colors.GRAY}None{Colors.RESET}"

    if isinstance(value, bool):
        return f"{Colors.GREEN if value else Colors.RED}{value}{Colors.RESET}"

    if isinstance(value, (int, float)):
        return f"{Colors.CYAN}{value!r}{Colors.RESET}"

    if isinstance(value, str):
        return f"{Colors.YELLOW}{value!r}{Colors.RESET}"

    if isinstance(value, Enum):
        return (
            f"{Colors.PURPLE}{value.__class__.__name__}.{value.name}"
            f"{Colors.RESET}"
        )

    if isinstance(value, bytes):
        snippet = repr(value[:32]) + ("..." if len(value) > 32 else "")  # noqa: PLR2004
        return (
            f"{Colors.BLUE}{snippet}{Colors.RESET}"
            f" {Colors.GRAY}(len={len(value)}){Colors.RESET}"
        )

    if isinstance(value, Struct):
        indent = _INDENT * level
        next_indent = _INDENT * (level + 1)
        lines = [
            f"{Colors.PURPLE}{value.__class__.__name__}{Colors.GRAY}{{{Colors.RESET}"
        ]

        for field in get_struct_fields(value):
            f_val = getattr(value, field.name)
            lines.append(
                f"{next_indent}{Colors.CYAN_BRIGHT}{field.name}{Colors.RESET}:"
                f" {_format_value(f_val, level + 1)},"
            )

        if len(lines) > 1:
            lines[-1] = lines[-1].rstrip(",")
        lines.append(f"{indent}{Colors.GRAY}}}{Colors.RESET}")
        return "\n".join(lines)

    if isinstance(value, (list, tuple)):
        if not value:
            return f"{Colors.GRAY}[]{Colors.RESET}"
        items = ", ".join(_format_value(x, 0) for x in value[:10])
        return (
            f"{Colors.GRAY}[{Colors.RESET} {items} {Colors.GRAY}]"
            f"{Colors.RESET}"
        )

    if isinstance(value, dict):
        return f"{Colors.GRAY}{{{Colors.RESET}...{Colors.GRAY}}}{Colors.RESET}"

    return repr(value)


def format_packet(packet: "Packet") -> str:
    lines = [
        f"\n{Colors.GREEN_BOLD}({packet.__class__.__name__}){Colors.RESET}:"
    ]

    lines.append(
        f"{_INDENT}({Colors.GREEN}VarInt{Colors.RESET}) "
        f"{Colors.CYAN_BRIGHT}packet_id{Colors.RESET}: {Colors.CYAN}"
        f"{packet.packet_id:#04x}{Colors.RESET},"
    )

    for field in packet.get_schema():
        val = getattr(packet, field.name)
        codec_name = field.codec.__class__.__name__.removesuffix("Codec")
        formatted_val = _format_value(val, level=1)

        lines.append(
            f"{_INDENT}({Colors.GREEN}{codec_name}{Colors.RESET}) "
            f"{Colors.CYAN_BRIGHT}{field.name}{Colors.RESET}: {formatted_val},"
        )

    if len(lines) > 1:
        lines[-1] = lines[-1].rstrip(",")

    return "\n".join(lines)
