from typing import Any, ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import TextComponent, VarInt


class DisguisedChatMessage(Packet, kw_only=True):
    """Packet representing DisguisedChatMessage (Auto-generated)."""

    __state__ = State.PLAY
    __direction__ = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x21

    message: TextComponent
    """
    Text Component - This is used as thecontentparameter when formatting
    the message on the client.
    """

    chat_type: Any  # TODO: ID orChat Type
    """
    ID orChat Type - Either the type of chat in
    theminecraft:chat_typeregistry, defined by theRegistry Datapacket, or
    an inline definition.
    """

    sender_name: TextComponent
    """
    Text Component - The name of the one sending the message, usually the
    sender's display name.This is used as thesenderparameter when
    formatting the message on the client.
    """

    target_name: TextComponent | None = None
    """
    Prefixed OptionalText Component - The name of the one receiving the
    message, usually the receiver's display name.This is used as
    thetargetparameter when formatting the message on the client.
    """
