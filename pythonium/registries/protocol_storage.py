import json
from pathlib import Path

from pythonium.engine.enums import Direction, State

PROTOCOL_PATH = Path(__file__).parent / "protocol.json"


def load_protocol_registry() -> dict[str, tuple[State, Direction, int]]:
    with PROTOCOL_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    registry = {}

    for full_key, info in data.items():
        direction_str: str = info[0]
        state_str: str = info[1]
        packet_id: int = info[2]

        state_enum = State[state_str.upper()]
        direction_enum = Direction[direction_str.upper()]

        registry[full_key] = (state_enum, direction_enum, packet_id)

    return registry


PROTOCOL_REGISTRY = load_protocol_registry()


def get_data_by_packet_name(packet_name: str) -> tuple[State, Direction, int]:
    return PROTOCOL_REGISTRY[packet_name]
