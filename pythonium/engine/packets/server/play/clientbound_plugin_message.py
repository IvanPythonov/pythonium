from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Identifier, VarInt


class ClientboundPluginMessage(Packet, kw_only=True):
    """Packet representing ClientboundPluginMessage (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x18

    channel: Identifier
    """Identifier - Name of theplugin channelused to send the data."""

    data: Any  # TODO: Byte Array(1048576)
    """
    Byte Array(1048576) - Any data, depending on the channel. Typically
    this would be a sequence of fields using standard data types, but some
    unofficial channels have unusual formats. There is no length prefix
    that applies to all channel types, but the format specific to the
    channel may or may not include one or more length prefixes (such as the
    string length prefix in the standardminecraft:brandchannel). The
    vanilla client enforces a length limit of 1048576 bytes on this data,
    but only if the channel type is unrecognized.
    """
