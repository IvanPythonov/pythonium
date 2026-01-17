from enum import StrEnum
from typing import TYPE_CHECKING, Any

from pythonium.engine.codecs import Codec, OptionalCodec

if TYPE_CHECKING:
    from pythonium.engine.packets.base import Packet

_INDENT = "    "


class Colors(StrEnum):
    """Colors enumeration."""

    GREEN_BOLD = "\033[1;32m"
    GRAY = "\033[90m"
    CYAN_BRIGHT = "\033[96m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[36m"
    RESET = "\033[0m"


def _get_codec_name(codec: Codec[Any]) -> str:
    match codec:
        case OptionalCodec():
            return f"Optional[{_get_codec_name(codec.inner_codec)}]"
        case _:
            return codec.__class__.__name__.removesuffix("Codec")


def _format_value(value: Any) -> str:  # noqa: ANN401
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
    return repr(value)


def _format_field(name: str, value: Any, codec: Codec[Any]) -> str:  # noqa: ANN401
    codec_name = _get_codec_name(codec)
    formatted_value = _format_value(value)
    return (
        f"{_INDENT}{Colors.GRAY}({codec_name}){Colors.RESET} "
        f"{Colors.CYAN_BRIGHT}{name}{Colors.RESET}: {formatted_value}"
    )


def format_packet(packet: "Packet") -> str:
    lines: list[str] = [
        f"\n{Colors.GREEN_BOLD}({packet.__class__.__name__}):{Colors.RESET}"
    ]

    packet_id_value = f"{Colors.CYAN}{hex(packet.packet_id)}{Colors.RESET}"
    lines.append(
        f"{_INDENT}{Colors.GRAY}(VarInt){Colors.RESET} "
        f"{Colors.CYAN_BRIGHT}packet_id{Colors.RESET}: {packet_id_value},"
    )

    for field in packet.__schema__:
        value = getattr(packet, field.name)

        lines.append(_format_field(field.name, value, field.codec) + ",")

    lines[-1] = lines[-1].rstrip(",")

    return "\n".join(lines)
