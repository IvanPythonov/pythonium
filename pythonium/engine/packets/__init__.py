from pythonium.engine.enums import Direction, State

from .base import Packet, deserialize, serialize
from .client.configuration import (
    AcknowledgeFinishConfiguration,
    ClientInformation,
    ConfigurationCustomPayload,
    KeepAliveConfigurationRequest,
    PongConfiguration,
)
from .client.handshake import Handshake
from .client.login import LoginAcknowledged, LoginCustomPayload, LoginStart
from .client.play import Login
from .client.status import GetStatus, Ping
from .packet_storage import PacketStorage
from .server.configuration import (
    Disconnect,
    FinishConfiguration,
    KeepAliveConfigurationResponse,
    PingConfiguration,
)
from .server.login import LoginSuccess
from .server.status import Pong, ServerStatus

__all__ = (
    "AcknowledgeFinishConfiguration",
    "ClientInformation",
    "ConfigurationCustomPayload",
    "Disconnect",
    "FinishConfiguration",
    "GetStatus",
    "Handshake",
    "KeepAliveConfigurationRequest",
    "KeepAliveConfigurationResponse",
    "Login",
    "LoginAcknowledged",
    "LoginCustomPayload",
    "LoginStart",
    "LoginSuccess",
    "Packet",
    "PacketStorage",
    "Ping",
    "PingConfiguration",
    "Pong",
    "PongConfiguration",
    "ServerStatus",
    "deserialize",
    "serialize",
)


def get_model_by_id(
    packet_id: int, state: State, direction: Direction
) -> type[Packet]:
    """Get model by prefix."""
    for model in Packet.__subclasses__():
        key = (packet_id, state, direction)
        if PacketStorage.get(*key) is model:
            return model

    msg = f"Unknown packet_id: {hex(packet_id)}"
    raise ValueError(msg)
