from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Slot, VarInt


class SetContainerContent(Packet, kw_only=True):
    """Packet representing SetContainerContent (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x12

    window_id: VarInt
    """
    VarInt - The ID of window which items are being sent for. 0 for player
    inventory. The client ignores any packets targeting a Window ID other
    than the current one. However, an exception is made for the player
    inventory, which may be targeted at any time. (The vanilla server does
    not appear to utilize this special case.)
    """

    state_id: VarInt
    """
    VarInt - A server-managed sequence number used to avoid
    desynchronization; see#Click Container.
    """

    slot_data: Any  # TODO: Prefixed ArrayofSlot
    """Prefixed ArrayofSlot"""

    carried_item: Slot
    """Slot - Item being dragged with the mouse."""
