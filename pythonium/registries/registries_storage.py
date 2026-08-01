from pathlib import Path
from typing import Any, Self

import msgspec
from nbtlib import Base, Byte, Compound, Double, Int, List, String

from pythonium.engine.packets.outgoing import RegistryData
from pythonium.registries.base import Registry

_PRIMITIVE_FACTORY = {
    int: Int,
    float: Double,
    str: String,
    bool: lambda v: Byte(1 if v else 0),
}


def _convert_value(value: object) -> Base:
    if isinstance(value, dict):
        return Compound({k: _convert_value(v) for k, v in value.items()})

    if isinstance(value, list):
        if not value:
            return List[String]()

        converted = [_convert_value(v) for v in value]
        return List[type(converted[0])](converted)

    if isinstance(value, (int, float, str, bool)):
        return _PRIMITIVE_FACTORY[type(value)](value)

    if value is None:
        return Compound({})

    return String(str(value))


def json_to_nbt(json_data: dict[str, Any]) -> Compound:
    return _convert_value(json_data)


class RegistryRegistry(Registry[RegistryData]):
    """Registry data registry."""

    __registry_path__ = Path(__file__).parent / "registries.json"

    def discover(self) -> Self:
        data: dict[str, dict[str, Any]] = msgspec.json.decode(
            self.__registry_path__.read_bytes()
        )

        for registry_id, entries_dict in data.items():
            entries: list[tuple[str, Compound | None]] = []

            for entry_id, entry_data in entries_dict.items():
                entries.append(
                    (
                        entry_id,
                        json_to_nbt(entry_data),
                    )
                )

            self.register(
                registry_id,
                RegistryData(
                    registry_id=registry_id,
                    entries=entries,
                ),
            )

        return self


REGISTRY_REGISTRY = RegistryRegistry().discover()
