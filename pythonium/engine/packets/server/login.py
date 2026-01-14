from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets import Packet
from pythonium.engine.types import UUID, Boolean, String, VarInt


class LoginSuccess(Packet, kw_only=True):
    """Packet representing login success."""

    __state__ = State.LOGIN
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x02

    uuid: UUID
    name: String
    is_legacy: Boolean
