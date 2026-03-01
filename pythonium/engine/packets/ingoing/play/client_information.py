from typing import ClassVar

from pythonium.engine.enums import Direction, State
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import Boolean, Byte, String, UByte, VarInt


class ClientInformation(Packet, kw_only=True):
    """Packet representing ClientInformation (Auto-generated)."""

    __state__: ClassVar[State] = State.PLAY
    __direction__: ClassVar[Direction] = Direction.SERVERBOUND

    packet_id: ClassVar[VarInt] = 0x0D

    locale: String
    """String(16) - e.g.en_GB."""

    view_distance: Byte
    """Byte - Client-side render distance, in chunks."""

    chat_mode: VarInt
    """
    VarIntEnum - 0: enabled, 1: commands only, 2: hidden.  SeeJava Edition
    protocol/Chat#Client chat modefor more information.
    """

    chat_colors: Boolean
    """
    Boolean - “Colors” multiplayer setting. The vanilla server stores this
    value but does nothing with it (seeMC-64867). Some third-party servers
    disable all coloring in chat and system messages when it is false.
    """

    displayed_skin_parts: UByte
    """Unsigned Byte - Bit mask, see below."""

    main_hand: VarInt
    """VarIntEnum - 0: Left, 1: Right."""

    enable_text_filtering: Boolean
    """
    Boolean - Enables filtering of text on signs and written book titles.
    The vanilla client sets this according to
    theprofanityFilterPreferences.profanityFilterOnaccount attribute
    indicated by theMojang API endpoint for player attributes. In offline
    mode, it is always false.
    """

    allow_server_listings: Boolean
    """
    Boolean - Servers usually list online players; this option should let
    you not show up in that list.
    """

    particle_status: VarInt
    """VarIntEnum - 0: all, 1: decreased, 2: minimal"""
