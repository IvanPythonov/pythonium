from pathlib import Path

from nbtlib import parse_nbt

from pythonium.engine.packets import RegistryData

REGISTRIES_FILE = Path(__file__).parent / "registries.snbt"
REGISTRIES_NBT = parse_nbt(REGISTRIES_FILE.read_text(encoding="utf-8"))


def build_registry_packets() -> list[RegistryData]:
    packets = []

    for registry_id, entries_nbt in REGISTRIES_NBT.items():
        entries = []

        for entry_id, entry_data in entries_nbt.items():
            entries.append((entry_id, entry_data))

        packets.append(RegistryData(registry_id=registry_id, entries=entries))

    return packets


REGISTRY_PACKETS = build_registry_packets()
