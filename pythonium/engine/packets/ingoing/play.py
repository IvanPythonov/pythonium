from typing import ClassVar

from pythonium.engine.enums.action_id import ActionId
from pythonium.engine.enums.block_action import BlockActionStatus, Rotation
from pythonium.engine.enums.difficulty import DifficultyEnum
from pythonium.engine.enums.gamemode import GameMode
from pythonium.engine.enums.placement import PlacementFlags
from pythonium.engine.enums.use_entity import Hand, UseEntityAction
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import (
    UUID,
    ArgumentSignatureArray,
    Boolean,
    Byte,
    ByteArray,
    ChangedSlotArray,
    Double,
    FixedBitSet20,
    Float,
    HashedSlot,
    Int,
    Long,
    OptionalByteArray,
    OptionalFloat,
    OptionalIdentifier,
    OptionalString,
    OptionalVarInt,
    PrefixedOptionalTextComponent,
    RestBuffer,
    Short,
    Slot,
    String,
    StringArray,
    UByte,
    VarInt,
    VarLong,
)
from pythonium.engine.types import (
    Position as PositionType,
)


class TeleportConfirm(Packet, kw_only=True):
    """Packet representing TeleportConfirm."""

    __packet_name__: ClassVar[str] = "play:serverbound:teleport_confirm"

    teleport_id: VarInt


class QueryBlockNbt(Packet, kw_only=True):
    """Packet representing QueryBlockNbt."""

    __packet_name__: ClassVar[str] = "play:serverbound:query_block_nbt"

    transaction_id: VarInt
    location: PositionType


class SelectBundleItem(Packet, kw_only=True):
    """Packet representing SelectBundleItem."""

    __packet_name__: ClassVar[str] = "play:serverbound:select_bundle_item"

    slot_id: VarInt
    selected_item_index: VarInt


class SetDifficulty(Packet, kw_only=True):
    """Packet representing SetDifficulty."""

    __packet_name__: ClassVar[str] = "play:serverbound:set_difficulty"

    new_difficulty: DifficultyEnum


class ChangeGamemode(Packet, kw_only=True):
    """Packet representing ChangeGamemode."""

    __packet_name__: ClassVar[str] = "play:serverbound:change_gamemode"

    mode: GameMode


class MessageAcknowledgement(Packet, kw_only=True):
    """Packet representing MessageAcknowledgement."""

    __packet_name__: ClassVar[str] = "play:serverbound:message_acknowledgement"

    count: VarInt


class ChatCommand(Packet, kw_only=True):
    """Packet representing ChatCommand."""

    __packet_name__: ClassVar[str] = "play:serverbound:chat_command"

    command: String


class ChatCommandSigned(Packet, kw_only=True):
    """Packet representing ChatCommandSigned."""

    __packet_name__: ClassVar[str] = "play:serverbound:chat_command_signed"

    command: String
    timestamp: Long
    salt: Long
    argument_signatures: ArgumentSignatureArray
    message_count: VarInt
    acknowledged: FixedBitSet20
    checksum: Byte


class ChatMessage(Packet, kw_only=True):
    """Packet representing ChatMessage."""

    __packet_name__: ClassVar[str] = "play:serverbound:chat_message"

    message: String
    timestamp: Long
    salt: Long
    signature: OptionalByteArray

    offset: VarInt

    acknowledged: FixedBitSet20
    checksum: Byte


class ChatSessionUpdate(Packet, kw_only=True):
    """Packet representing ChatSessionUpdate."""

    __packet_name__: ClassVar[str] = "play:serverbound:chat_session_update"

    session_uuid: UUID
    expire_time: Long
    public_key: ByteArray
    signature: ByteArray


class ChunkBatchReceived(Packet, kw_only=True):
    """Packet representing ChunkBatchReceived."""

    __packet_name__: ClassVar[str] = "play:serverbound:chunk_batch_received"

    chunks_per_tick: Float


class ClientCommand(Packet, kw_only=True):
    """Packet representing ClientCommand."""

    __packet_name__: ClassVar[str] = "play:serverbound:client_command"

    action_id: VarInt


class TickEnd(Packet, kw_only=True):
    """Packet representing TickEnd."""

    __packet_name__: ClassVar[str] = "play:serverbound:tick_end"


class Settings(Packet, kw_only=True):
    """Packet representing Settings."""

    __packet_name__: ClassVar[str] = "play:serverbound:settings"


class TabComplete(Packet, kw_only=True):
    """Packet representing TabComplete."""

    __packet_name__: ClassVar[str] = "play:serverbound:tab_complete"

    transaction_id: VarInt

    text: String


class ConfigurationAcknowledged(Packet, kw_only=True):
    """Packet representing ConfigurationAcknowledged."""

    __packet_name__: ClassVar[str] = (
        "play:serverbound:configuration_acknowledged"
    )


class EnchantItem(Packet, kw_only=True):
    """Packet representing EnchantItem."""

    __packet_name__: ClassVar[str] = "play:serverbound:enchant_item"

    window_id: VarInt
    enchantment: Byte


class WindowClick(Packet, kw_only=True):
    """Packet representing WindowClick."""

    __packet_name__: ClassVar[str] = "play:serverbound:window_click"

    window_id: VarInt
    state_id: VarInt
    slot: Short
    mouse_button: Byte
    mode: VarInt

    changed_slots: ChangedSlotArray

    cursor_item: HashedSlot


class CloseWindow(Packet, kw_only=True):
    """Packet representing CloseWindow."""

    __packet_name__: ClassVar[str] = "play:serverbound:close_window"

    window_id: VarInt


class SetSlotState(Packet, kw_only=True):
    """Packet representing SetSlotState."""

    __packet_name__: ClassVar[str] = "play:serverbound:set_slot_state"

    slot_id: VarInt
    window_id: VarInt
    state_: Boolean


class CookieResponse(Packet, kw_only=True):
    """Packet representing CookieResponse."""

    __packet_name__: ClassVar[str] = "play:serverbound:cookie_response"


class CustomPayload(Packet, kw_only=True):
    """Packet representing CustomPayload."""

    __packet_name__: ClassVar[str] = "play:serverbound:custom_payload"

    channel: String
    data: RestBuffer


class DebugSampleSubscription(Packet, kw_only=True):
    """Packet representing DebugSampleSubscription."""

    __packet_name__: ClassVar[str] = (
        "play:serverbound:debug_sample_subscription"
    )

    type_: VarInt


class EditBook(Packet, kw_only=True):
    """Packet representing EditBook."""

    __packet_name__: ClassVar[str] = "play:serverbound:edit_book"

    hand: VarInt
    pages: StringArray
    title: OptionalString


class QueryEntityNbt(Packet, kw_only=True):
    """Packet representing QueryEntityNbt."""

    __packet_name__: ClassVar[str] = "play:serverbound:query_entity_nbt"

    transaction_id: VarInt
    entity_id: VarInt


class UseEntity(Packet, kw_only=True):
    """Packet representing UseEntity."""

    __packet_name__: ClassVar[str] = "play:serverbound:use_entity"

    target: VarInt
    mouse: UseEntityAction

    x: OptionalFloat
    y: OptionalFloat
    z: OptionalFloat

    hand: Hand

    sneaking: Boolean


class GenerateStructure(Packet, kw_only=True):
    """Packet representing GenerateStructure."""

    __packet_name__: ClassVar[str] = "play:serverbound:generate_structure"

    location: PositionType
    levels: VarInt
    keep_jigsaws: Boolean


class KeepAlive(Packet, kw_only=True):
    """Packet representing KeepAlive."""

    __packet_name__: ClassVar[str] = "play:serverbound:keep_alive"

    keep_alive_id: Long


class LockDifficulty(Packet, kw_only=True):
    """Packet representing LockDifficulty."""

    __packet_name__: ClassVar[str] = "play:serverbound:lock_difficulty"

    locked: Boolean


class Position(Packet, kw_only=True):
    """Packet representing Position."""

    __packet_name__: ClassVar[str] = "play:serverbound:position"

    x: Double
    y: Double
    z: Double
    on_ground: Boolean


class PositionLook(Packet, kw_only=True):
    """Packet representing PositionLook."""

    __packet_name__: ClassVar[str] = "play:serverbound:position_look"

    x: Double
    y: Double
    z: Double
    yaw: Float
    pitch: Float
    on_ground: Boolean


class Look(Packet, kw_only=True):
    """Packet representing Look."""

    __packet_name__: ClassVar[str] = "play:serverbound:look"

    yaw: Float
    pitch: Float
    on_ground: Boolean


class Flying(Packet, kw_only=True):
    """Packet representing Flying."""

    __packet_name__: ClassVar[str] = "play:serverbound:flying"

    on_ground: Boolean


class VehicleMove(Packet, kw_only=True):
    """Packet representing VehicleMove."""

    __packet_name__: ClassVar[str] = "play:serverbound:vehicle_move"

    x: Double
    y: Double
    z: Double
    yaw: Float
    pitch: Float
    on_ground: Boolean


class SteerBoat(Packet, kw_only=True):
    """Packet representing SteerBoat."""

    __packet_name__: ClassVar[str] = "play:serverbound:steer_boat"

    left_paddle: Boolean
    right_paddle: Boolean


class PickItemFromBlock(Packet, kw_only=True):
    """Packet representing PickItemFromBlock."""

    __packet_name__: ClassVar[str] = "play:serverbound:pick_item_from_block"

    position: PositionType
    include_data: Boolean


class PickItemFromEntity(Packet, kw_only=True):
    """Packet representing PickItemFromEntity."""

    __packet_name__: ClassVar[str] = "play:serverbound:pick_item_from_entity"

    entity_id: VarInt
    include_data: Boolean


class PingRequest(Packet, kw_only=True):
    """Packet representing PingRequest."""

    __packet_name__: ClassVar[str] = "play:serverbound:ping_request"

    id_: Long


class CraftRecipeRequest(Packet, kw_only=True):
    """Packet representing CraftRecipeRequest."""

    __packet_name__: ClassVar[str] = "play:serverbound:craft_recipe_request"

    window_id: VarInt
    recipe_id: VarInt
    make_all: Boolean


class Abilities(Packet, kw_only=True):
    """Packet representing Abilities."""

    __packet_name__: ClassVar[str] = "play:serverbound:abilities"

    flags: Byte


class BlockDig(Packet, kw_only=True):
    """Packet representing BlockDig."""

    __packet_name__: ClassVar[str] = "play:serverbound:block_dig"

    status: VarInt
    location: PositionType
    face: Byte
    sequence: VarInt


class EntityAction(Packet, kw_only=True):
    """Packet representing EntityAction."""

    __packet_name__: ClassVar[str] = "play:serverbound:entity_action"

    entity_id: VarInt
    action_id: ActionId

    jump_boost: VarInt


class PlayerInput(Packet, kw_only=True):
    """Packet representing PlayerInput."""

    __packet_name__: ClassVar[str] = "play:serverbound:player_input"

    inputs: Byte


class PlayerLoaded(Packet, kw_only=True):
    """Packet representing PlayerLoaded."""

    __packet_name__: ClassVar[str] = "play:serverbound:player_loaded"


class Pong(Packet, kw_only=True):
    """Packet representing Pong."""

    __packet_name__: ClassVar[str] = "play:serverbound:pong"

    id_: Int


class RecipeBook(Packet, kw_only=True):
    """Packet representing RecipeBook."""

    __packet_name__: ClassVar[str] = "play:serverbound:recipe_book"

    book_id: VarInt
    book_open: Boolean
    filter_active: Boolean


class DisplayedRecipe(Packet, kw_only=True):
    """Packet representing DisplayedRecipe."""

    __packet_name__: ClassVar[str] = "play:serverbound:displayed_recipe"

    recipe_id: VarInt


class NameItem(Packet, kw_only=True):
    """Packet representing NameItem."""

    __packet_name__: ClassVar[str] = "play:serverbound:name_item"

    name: String


class ResourcePackReceive(Packet, kw_only=True):
    """Packet representing ResourcePackReceive."""

    __packet_name__: ClassVar[str] = "play:serverbound:resource_pack_receive"

    uuid: UUID
    result: VarInt


class AdvancementTab(Packet, kw_only=True):
    """Packet representing AdvancementTab."""

    __packet_name__: ClassVar[str] = "play:serverbound:advancement_tab"

    action: VarInt  # 0: Opened tab, 1: Closed screen.
    tab_id: OptionalIdentifier  # Only present if action is Opened tab.


class SelectTrade(Packet, kw_only=True):
    """Packet representing SelectTrade."""

    __packet_name__: ClassVar[str] = "play:serverbound:select_trade"

    slot: VarInt


class SetBeaconEffect(Packet, kw_only=True):
    """Packet representing SetBeaconEffect."""

    __packet_name__: ClassVar[str] = "play:serverbound:set_beacon_effect"

    primary_effect: OptionalVarInt
    secondary_effect: OptionalVarInt


class HeldItemSlot(Packet, kw_only=True):
    """Packet representing HeldItemSlot."""

    __packet_name__: ClassVar[str] = "play:serverbound:held_item_slot"

    slot_id: Short


class UpdateCommandBlock(Packet, kw_only=True):
    """Packet representing UpdateCommandBlock."""

    __packet_name__: ClassVar[str] = "play:serverbound:update_command_block"

    location: PositionType
    command: String
    mode: VarInt
    flags: UByte


class UpdateCommandBlockMinecart(Packet, kw_only=True):
    """Packet representing UpdateCommandBlockMinecart."""

    __packet_name__: ClassVar[str] = (
        "play:serverbound:update_command_block_minecart"
    )

    entity_id: VarInt
    command: String
    track_output: Boolean


class SetCreativeSlot(Packet, kw_only=True):
    """Packet representing SetCreativeSlot."""

    __packet_name__: ClassVar[str] = "play:serverbound:set_creative_slot"

    slot: Short
    item: Slot


class UpdateJigsawBlock(Packet, kw_only=True):
    """Packet representing UpdateJigsawBlock."""

    __packet_name__: ClassVar[str] = "play:serverbound:update_jigsaw_block"

    location: PositionType
    name: String
    target: String
    pool: String
    final_state: String
    joint_type: String
    selection_priority: VarInt
    placement_priority: VarInt


class UpdateStructureBlock(Packet, kw_only=True):
    """Packet representing UpdateStructureBlock."""

    __packet_name__: ClassVar[str] = "play:serverbound:update_structure_block"

    location: PositionType
    action: VarInt
    mode: VarInt
    name: String

    offset_x: Byte
    offset_y: Byte
    offset_z: Byte

    size_x: Byte
    size_y: Byte
    size_z: Byte

    mirror: VarInt
    rotation: VarInt
    metadata: String
    integrity: Float
    seed: VarLong
    flags: PlacementFlags


class SetTestBlock(Packet, kw_only=True):
    """Packet representing SetTestBlock."""

    __packet_name__: ClassVar[str] = "play:serverbound:set_test_block"

    position: PositionType
    mode: VarInt
    message: String


class UpdateSign(Packet, kw_only=True):
    """Packet representing UpdateSign."""

    __packet_name__: ClassVar[str] = "play:serverbound:update_sign"

    location: PositionType

    is_front_text: Boolean

    text1: String
    text2: String
    text3: String
    text4: String


class ArmAnimation(Packet, kw_only=True):
    """Packet representing ArmAnimation."""

    __packet_name__: ClassVar[str] = "play:serverbound:arm_animation"

    hand: VarInt


class Spectate(Packet, kw_only=True):
    """Packet representing Spectate."""

    __packet_name__: ClassVar[str] = "play:serverbound:spectate"

    target: UUID


class TestInstanceBlockAction(Packet, kw_only=True):
    """Packet representing TestInstanceBlockAction."""

    __packet_name__: ClassVar[str] = (
        "play:serverbound:test_instance_block_action"
    )

    pos: PositionType
    action: VarInt

    test: OptionalIdentifier

    size_x: VarInt
    size_y: VarInt
    size_z: VarInt

    rotation: Rotation
    ignore_entities: Boolean
    status: BlockActionStatus

    error_message: PrefixedOptionalTextComponent


class BlockPlace(Packet, kw_only=True):
    """Packet representing BlockPlace."""

    __packet_name__: ClassVar[str] = "play:serverbound:block_place"

    hand: VarInt
    location: PositionType
    direction_: VarInt

    cursor_x: Float
    cursor_y: Float
    cursor_z: Float

    inside_block: Boolean

    world_border_hit: Boolean

    sequence: VarInt


class UseItem(Packet, kw_only=True):
    """Packet representing UseItem."""

    __packet_name__: ClassVar[str] = "play:serverbound:use_item"

    hand: VarInt
    sequence: VarInt
    yaw: Float
    pitch: Float


class CustomClickAction(Packet, kw_only=True):
    """Packet representing CustomClickAction."""

    __packet_name__: ClassVar[str] = "play:serverbound:custom_click_action"
