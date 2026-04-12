from typing import Annotated, ClassVar

from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.custom import StringCodec
from pythonium.engine.codecs.nbt import NBTCodec
from pythonium.engine.codecs.optional import OptionalCodec
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import (
    Identifier,
    Int,
    Long,
    NBTCompound,
    RestBuffer,
    String,
    StringArray,
    TagArray,
    TextComponent,
)

type IdentifierNBT = Annotated[
    list[tuple[str, NBTCompound | None]],
    ArrayCodec((StringCodec(), OptionalCodec(NBTCodec()))),
]


class CookieRequest(Packet, kw_only=True):
    """Packet representing CookieRequest."""

    __packet_name__: ClassVar[str] = "configuration:clientbound:cookie_request"


class CustomPayload(Packet, kw_only=True):
    """Packet representing CustomPayload."""

    __packet_name__: ClassVar[str] = "configuration:clientbound:custom_payload"

    channel: String
    data: RestBuffer


class Disconnect(Packet, kw_only=True):
    """Packet representing Disconnect."""

    __packet_name__: ClassVar[str] = "configuration:clientbound:disconnect"

    reason: TextComponent


class FinishConfiguration(Packet, kw_only=True):
    """Packet representing FinishConfiguration."""

    __packet_name__: ClassVar[str] = (
        "configuration:clientbound:finish_configuration"
    )


class KeepAlive(Packet, kw_only=True):
    """Packet representing KeepAlive."""

    __packet_name__: ClassVar[str] = "configuration:clientbound:keep_alive"

    keep_alive_id: Long


class Ping(Packet, kw_only=True):
    """Packet representing Ping."""

    __packet_name__: ClassVar[str] = "configuration:clientbound:ping"

    id_: Int


class ResetChat(Packet, kw_only=True):
    """Packet representing ResetChat."""

    __packet_name__: ClassVar[str] = "configuration:clientbound:reset_chat"


class RegistryData(Packet, kw_only=True):
    """Packet representing RegistryData."""

    __packet_name__: ClassVar[str] = "configuration:clientbound:registry_data"

    registry_id: Identifier
    entries: IdentifierNBT


class RemoveResourcePack(Packet, kw_only=True):
    """Packet representing RemoveResourcePack."""

    __packet_name__: ClassVar[str] = (
        "configuration:clientbound:remove_resource_pack"
    )


class AddResourcePack(Packet, kw_only=True):
    """Packet representing AddResourcePack."""

    __packet_name__: ClassVar[str] = (
        "configuration:clientbound:add_resource_pack"
    )


class StoreCookie(Packet, kw_only=True):
    """Packet representing StoreCookie."""

    __packet_name__: ClassVar[str] = "configuration:clientbound:store_cookie"


class Transfer(Packet, kw_only=True):
    """Packet representing Transfer."""

    __packet_name__: ClassVar[str] = "configuration:clientbound:transfer"


class FeatureFlags(Packet, kw_only=True):
    """Packet representing FeatureFlags."""

    __packet_name__: ClassVar[str] = "configuration:clientbound:feature_flags"

    features: StringArray


class Tags(Packet, kw_only=True):
    """Packet representing Tags."""

    __packet_name__: ClassVar[str] = "configuration:clientbound:tags"

    tags: TagArray


class SelectKnownPacks(Packet, kw_only=True):
    """Packet representing SelectKnownPacks."""

    __packet_name__: ClassVar[str] = (
        "configuration:clientbound:select_known_packs"
    )


class CustomReportDetails(Packet, kw_only=True):
    """Packet representing CustomReportDetails."""

    __packet_name__: ClassVar[str] = (
        "configuration:clientbound:custom_report_details"
    )


class ServerLinks(Packet, kw_only=True):
    """Packet representing ServerLinks."""

    __packet_name__: ClassVar[str] = "configuration:clientbound:server_links"


class ClearDialog(Packet, kw_only=True):
    """Packet representing ClearDialog."""

    __packet_name__: ClassVar[str] = "configuration:clientbound:clear_dialog"


class ShowDialog(Packet, kw_only=True):
    """Packet representing ShowDialog."""

    __packet_name__: ClassVar[str] = "configuration:clientbound:show_dialog"

    dialog: NBTCompound
