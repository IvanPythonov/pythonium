from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets import Packet
from pythonium.engine.types import (
    UUID,
    Boolean,
    JsonTextComponent,
    String,
    VarInt,
)


class LoginSuccess(Packet, kw_only=True):
    """Packet representing login success."""

    __state__: ClassVar[State] = State.LOGIN
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x02

    uuid: UUID
    name: String
    is_legacy: Boolean


class LoginDisconnect(Packet, kw_only=True):
    """Packet representing login disconnect."""

    __state__: ClassVar[State] = State.LOGIN
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x00

    reason: JsonTextComponent
