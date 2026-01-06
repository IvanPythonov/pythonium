from pythonium.engine.enums import State

from .base import Packet, deserialize, serialize
from .handshake import Handshake

__all__ = ("Handshake", "Packet", "deserialize", "serialize")


def get_model_by_id(
    packet_id: int, state: State = State.HANDSHAKING
) -> type[Packet]:
    """Get model by prefix."""
    for model in Packet.__subclasses__():
        if model.packet_id == packet_id and model.__state__ == state:
            return model

    msg = f"Unknown packet_id: {hex(packet_id)}"
    raise ValueError(msg)
