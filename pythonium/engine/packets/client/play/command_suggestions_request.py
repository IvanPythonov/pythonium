from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import String, VarInt


class CommandSuggestionsRequest(Packet, kw_only=True):
    """Packet representing CommandSuggestionsRequest (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x0E

    transaction_id: VarInt
    """
    VarInt - The ID of the transaction that the server will send back to
    the client in the response of this packet. Client generates this and
    increments it each time it sends another tab completion that doesn't
    get a response.
    """

    text: String
    """
    String(32500) - All the text behind the cursor including the/(e.g. to
    the left of the cursor in left-to-right languages like English).
    """
