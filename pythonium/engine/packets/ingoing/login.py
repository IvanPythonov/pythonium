from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets import Packet
from pythonium.engine.types import UUID, String, VarInt


class LoginStart(Packet, kw_only=True):
    """Packet representing login start."""

    __state__: ClassVar[State] = State.LOGIN
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x00

    name: String
    uuid: UUID


class LoginAcknowledged(Packet, kw_only=True):
    """Packet representing login acknowledged."""

    __state__: ClassVar[State] = State.LOGIN
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x03


class LoginCustomPayload(Packet, kw_only=True):
    """Packet representing login custom payload."""

    __state__: ClassVar[State] = State.LOGIN
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x02

    brand: String
    data: String
