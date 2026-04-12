from pathlib import Path
from typing import Any

import msgspec
from nbtlib import Base, Byte, Compound, Double, Int, List, String, parse_nbt

from pythonium.engine.packets.outgoing import RegistryData

REGISTRIES_FILE = Path(__file__).parent / "registries.json"
REGISTRIES_NBT = parse_nbt(REGISTRIES_FILE.read_text(encoding="utf-8"))


def _convert_value(value: Any) -> Base:
    if isinstance(value, dict):
        return Compound({k: _convert_value(v) for k, v in value.items()})

    if isinstance(value, list):
        if not value:
            return List[String]()

        converted_list = [_convert_value(v) for v in value]
        list_type = type(converted_list[0])
        return List[list_type](converted_list)

    if isinstance(value, bool):
        return Byte(1 if value else 0)

    if isinstance(value, int):
        return Int(value)

    if isinstance(value, float):
        return Double(value)

    if isinstance(value, str):
        return String(value)

    if value is None:
        return Compound({})

    return String(str(value))


def json_to_nbt(json_data: dict[str, Any]) -> Compound:
    return _convert_value(json_data)


def build_registry_packets() -> list[RegistryData]:
    packets: list[RegistryData] = []

    with REGISTRIES_FILE.open("r", encoding="utf-8") as f:
        registries_data: dict[str, dict[str, Any]] = msgspec.json.decode(
            f.read()
        )

    for registry_id, entries_dict in registries_data.items():
        entries: list[tuple[str, Compound | None]] = []

        for entry_id, entry_data in entries_dict.items():
            entry_nbt = json_to_nbt(entry_data)
            entries.append((entry_id, entry_nbt))

        packets.append(RegistryData(registry_id=registry_id, entries=entries))

    return packets


REGISTRY_PACKETS = build_registry_packets()
