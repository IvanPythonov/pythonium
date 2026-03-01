from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import VarInt


class ShowDialog(Packet, kw_only=True):
    """Packet representing ShowDialog (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x8A

    dialog: Any  # TODO: ID orNBT
    """
    ID orNBT - ID in theminecraft:dialogregistry, or an inline definition
    as described atDialog#Dialog format.
    """
