from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import UUID, Boolean, String, TextComponent, VarInt


class AddResourcePack(Packet, kw_only=True):
    """Packet representing AddResourcePack (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.CLIENTBOUND

    packet_id: ClassVar[VarInt] = 0x4F

    uuid: UUID
    """UUID - The unique identifier of the resource pack."""

    url: String
    """String(32767) - The URL to the resource pack."""

    hash: String
    """
    String(40) - A 40 character hexadecimal, case-insensitiveSHA-1hash of
    the resource pack file.If it's not a 40-character hexadecimal string,
    the client will not use it for hash verification and likely waste
    bandwidth.
    """

    forced: Boolean
    """
    Boolean - The vanilla client will be forced to use the resource pack
    from the server. If they decline, they will be kicked from the server.
    """

    prompt_message: TextComponent | None = None
    """
    Prefixed OptionalText Component - This is shown in the prompt making
    the client accept or decline the resource pack.
    """
