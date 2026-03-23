from typing import ClassVar

from pythonium.engine.enums.teleport_flags import TeleportFlags
from pythonium.engine.packets.base import Packet
from pythonium.engine.types import (
    UUID,
    AdvancementMappingArray,
    AttributePropertyArray,
    BlockEntityArray,
    Boolean,
    BossBarActionType,
    Byte,
    ByteArray,
    ChatType,
    ChunkBiomeDataArray,
    CommandMatchArray,
    Double,
    EquipmentArray,
    Float,
    HeightmapsArray,
    Identifier,
    IdentifierArray,
    Int,
    Light,
    LightData,
    Long,
    LongArray,
    MapColorPatch,
    MessageSignatureArray,
    MinecartStepArray,
    NBTCompound,
    OptionalBitSet,
    OptionalByteArray,
    OptionalDouble,
    OptionalDoubleVector,
    OptionalIdentifier,
    OptionalMapIconArray,
    OptionalString,
    OptionalVarInt,
    ParticleData,
    PlayerInfoUpdateData,
    PrefixedOptionalNumberFormat,
    PrefixedOptionalTextComponent,
    PrefixedOptionalWaypointColor,
    ProgressMappingArray,
    PropertySetArray,
    Recipe,
    RecipeDisplay,
    RestBuffer,
    Short,
    Slot,
    SlotArray,
    SoundEvent,
    StatisticArray,
    StonecutterRecipeArray,
    String,
    StringArray,
    TextComponent,
    TradeArray,
    UByte,
    UpdateObjectiveData,
    UpdateTeamData,
    UUIDArray,
    VarInt,
    VarIntArray,
    WaypointData,
    WorldState,
)
from pythonium.engine.types import (
    Position as PositionType,
)


class BundleDelimiter(Packet, kw_only=True):
    """Packet representing BundleDelimiter."""

    __packet_name__: ClassVar[str] = "play:clientbound:bundle_delimiter"


class SpawnEntity(Packet, kw_only=True):
    """Packet representing SpawnEntity."""

    __packet_name__: ClassVar[str] = "play:clientbound:spawn_entity"

    entity_id: VarInt
    object_uuid: UUID
    type_: VarInt
    x: Double
    y: Double
    z: Double
    pitch: Byte
    yaw: Byte
    head_pitch: Byte
    object_data: VarInt
    velocity_x: Short
    velocity_y: Short
    velocity_z: Short


class Animation(Packet, kw_only=True):
    """Packet representing Animation."""

    __packet_name__: ClassVar[str] = "play:clientbound:animation"

    entity_id: VarInt
    animation: UByte


class Statistics(Packet, kw_only=True):
    """Packet representing Statistics."""

    __packet_name__: ClassVar[str] = "play:clientbound:statistics"

    entries: StatisticArray


class AcknowledgePlayerDigging(Packet, kw_only=True):
    """Packet representing AcknowledgePlayerDigging."""

    __packet_name__: ClassVar[str] = (
        "play:clientbound:acknowledge_player_digging"
    )

    sequence_id: VarInt


class BlockBreakAnimation(Packet, kw_only=True):
    """Packet representing BlockBreakAnimation."""

    __packet_name__: ClassVar[str] = "play:clientbound:block_break_animation"

    entity_id: VarInt
    location: PositionType
    destroy_stage: Byte


class TileEntityData(Packet, kw_only=True):
    """Packet representing TileEntityData."""

    __packet_name__: ClassVar[str] = "play:clientbound:tile_entity_data"

    location: PositionType
    action: VarInt
    nbt_data: NBTCompound | None


class BlockAction(Packet, kw_only=True):
    """Packet representing BlockAction."""

    __packet_name__: ClassVar[str] = "play:clientbound:block_action"

    location: PositionType
    byte1: UByte
    byte2: UByte
    block_id: VarInt


class BlockChange(Packet, kw_only=True):
    """Packet representing BlockChange."""

    __packet_name__: ClassVar[str] = "play:clientbound:block_change"

    location: PositionType
    type_: VarInt


class BossBar(Packet, kw_only=True):
    """Packet representing BossBar."""

    __packet_name__: ClassVar[str] = "play:clientbound:boss_bar"

    entity_uuid: UUID
    action: BossBarActionType


class Difficulty(Packet, kw_only=True):
    """Packet representing Difficulty."""

    __packet_name__: ClassVar[str] = "play:clientbound:difficulty"

    difficulty: UByte  # TODO(IvanPythonov): make Unsigned Byte Enum
    # 0: peaceful, 1: easy, 2: normal, 3: hard.
    difficulty_locked: Boolean


class ChunkBatchFinished(Packet, kw_only=True):
    """Packet representing ChunkBatchFinished."""

    __packet_name__: ClassVar[str] = "play:clientbound:chunk_batch_finished"

    batch_size: VarInt


class ChunkBatchStart(Packet, kw_only=True):
    """Packet representing ChunkBatchStart."""

    __packet_name__: ClassVar[str] = "play:clientbound:chunk_batch_start"


class ChunkBiomes(Packet, kw_only=True):
    """Packet representing ChunkBiomes."""

    __packet_name__: ClassVar[str] = "play:clientbound:chunk_biomes"

    biomes: ChunkBiomeDataArray


class ClearTitles(Packet, kw_only=True):
    """Packet representing ClearTitles."""

    __packet_name__: ClassVar[str] = "play:clientbound:clear_titles"

    reset: Boolean


class TabComplete(Packet, kw_only=True):
    """Packet representing TabComplete."""

    __packet_name__: ClassVar[str] = "play:clientbound:tab_complete"

    transaction_id: VarInt
    start: VarInt
    length: VarInt
    matches: CommandMatchArray


class DeclareCommands(Packet, kw_only=True):
    """Packet representing DeclareCommands."""

    __packet_name__: ClassVar[str] = "play:clientbound:declare_commands"

    nodes: RestBuffer  # TODO(IvanPythonov): make Node codec cuz i too lazy
    # here was (root_index: VarInt) - 2026-2026


class CloseWindow(Packet, kw_only=True):
    """Packet representing CloseWindow."""

    __packet_name__: ClassVar[str] = "play:clientbound:close_window"

    window_id: VarInt


class WindowItems(Packet, kw_only=True):
    """Packet representing WindowItems."""

    __packet_name__: ClassVar[str] = "play:clientbound:window_items"

    window_id: VarInt
    state_id: VarInt
    items: SlotArray
    carried_item: Slot


class CraftProgressBar(Packet, kw_only=True):
    """Packet representing CraftProgressBar."""

    __packet_name__: ClassVar[str] = "play:clientbound:craft_progress_bar"

    window_id: VarInt
    property: Short
    value: Short


class SetSlot(Packet, kw_only=True):
    """Packet representing SetSlot."""

    __packet_name__: ClassVar[str] = "play:clientbound:set_slot"

    window_id: VarInt
    state_id: VarInt
    slot: Short
    item: Slot


class CookieRequest(Packet, kw_only=True):
    """Packet representing CookieRequest."""

    __packet_name__: ClassVar[str] = "play:clientbound:cookie_request"


class SetCooldown(Packet, kw_only=True):
    """Packet representing SetCooldown."""

    __packet_name__: ClassVar[str] = "play:clientbound:set_cooldown"

    cooldown_group: String
    cooldown_ticks: VarInt


class ChatSuggestions(Packet, kw_only=True):
    """Packet representing ChatSuggestions."""

    __packet_name__: ClassVar[str] = "play:clientbound:chat_suggestions"

    action: VarInt
    entries: StringArray


class CustomPayload(Packet, kw_only=True):
    """Packet representing CustomPayload."""

    __packet_name__: ClassVar[str] = "play:clientbound:custom_payload"

    channel: String
    data: RestBuffer


class DamageEvent(Packet, kw_only=True):
    """Packet representing DamageEvent."""

    __packet_name__: ClassVar[str] = "play:clientbound:damage_event"

    entity_id: VarInt
    source_type_id: VarInt
    source_cause_id: VarInt
    source_direct_id: VarInt
    source_position: OptionalDoubleVector


class DebugSample(Packet, kw_only=True):
    """Packet representing DebugSample."""

    __packet_name__: ClassVar[str] = "play:clientbound:debug_sample"

    sample: LongArray
    type_: VarInt


class HideMessage(Packet, kw_only=True):
    """Packet representing HideMessage."""

    __packet_name__: ClassVar[str] = "play:clientbound:hide_message"

    id_: VarInt
    signature: OptionalByteArray


class KickDisconnect(Packet, kw_only=True):
    """Packet representing KickDisconnect."""

    __packet_name__: ClassVar[str] = "play:clientbound:kick_disconnect"

    reason: TextComponent


class ProfilelessChat(Packet, kw_only=True):
    """Packet representing ProfilelessChat."""

    __packet_name__: ClassVar[str] = "play:clientbound:profileless_chat"

    message: TextComponent
    type_: ChatType
    name: TextComponent
    target: PrefixedOptionalTextComponent


class EntityStatus(Packet, kw_only=True):
    """Packet representing EntityStatus."""

    __packet_name__: ClassVar[str] = "play:clientbound:entity_status"

    entity_id: Int
    entity_status: Byte


class SyncEntityPosition(Packet, kw_only=True):
    """Packet representing SyncEntityPosition."""

    __packet_name__: ClassVar[str] = "play:clientbound:sync_entity_position"

    entity_id: VarInt
    x: Double
    y: Double
    z: Double
    dx: Double
    dy: Double
    dz: Double
    yaw: Float
    pitch: Float
    on_ground: Boolean


class Explosion(Packet, kw_only=True):
    """Packet representing Explosion."""

    __packet_name__: ClassVar[str] = "play:clientbound:explosion"

    x: Double
    y: Double
    z: Double
    player_knockback: OptionalDoubleVector
    explosion_particle: ParticleData
    sound: SoundEvent


class UnloadChunk(Packet, kw_only=True):
    """Packet representing UnloadChunk."""

    __packet_name__: ClassVar[str] = "play:clientbound:unload_chunk"

    chunk_z: Int
    chunk_x: Int


class GameStateChange(Packet, kw_only=True):
    """Packet representing GameStateChange."""

    __packet_name__: ClassVar[str] = "play:clientbound:game_state_change"

    reason: VarInt  # TODO(IvanPythonov): make enums
    game_mode: Float


# Event 	Effect 	Value
# 0 	No respawn block available 	Note: Displays message 'block.minecraft.
# spawn.not_valid' (You have no home bed or charged respawn anchor, or it was
# obstructed) to the player.
# 1 	Begin raining
# 2 	End raining
# 3 	Change game mode  0: Survival, 1: Creative, 2: Adventure, 3: Spectator.
# 4 	Win game 	0: Just respawn player.
# 1: Roll the credits and respawn player.
# Note that 1 is only sent by vanilla server when player has not yet achieved
# advancement "The end?", else 0 is sent.
# 5 	Demo event 	0: Show welcome to demo screen.
# 101: Tell movement controls.
# 102: Tell jump control.
# 103: Tell inventory control.
# 104: Tell that the demo is over and print a message about how to take a
# screenshot.
# 6 	Arrow hit player 	Note: Sent when any player is struck by an arrow.
# 7 	Rain level change 	Note: Seems to change both sky color and lighting.
# Rain level ranging from 0 to 1.
# 8 	Thunder level change 	Note: Seems to change both sky color and
# lighting (same as Rain level change, but doesn't start rain).
# It also requires rain to render by vanilla client.
# Thunder level ranging from 0 to 1.
# 9 	Play pufferfish sting sound
# 10 	Play elder guardian mob appearance (effect and sound)
# 11 	Enable respawn screen 	0: Enable respawn screen.
# 1: Immediately respawn (sent when the doImmediateRespawn gamerule changes).
# 12 	Limited crafting 	0: Disable limited crafting.
# 1: Enable limited crafting (sent when the doLimitedCrafting gamerule changes)
# 13 	Start waiting for level chunks
# Instructs the client to begin the waiting process for the level chunks.
# Sent by the server after the level is cleared on the client and is being
# re-sent (either during the first, or subsequent reconfigurations).


class OpenHorseWindow(Packet, kw_only=True):
    """Packet representing OpenHorseWindow."""

    __packet_name__: ClassVar[str] = "play:clientbound:open_horse_window"

    window_id: VarInt
    nb_slots: VarInt
    entity_id: Int


class HurtAnimation(Packet, kw_only=True):
    """Packet representing HurtAnimation."""

    __packet_name__: ClassVar[str] = "play:clientbound:hurt_animation"

    entity_id: VarInt
    yaw: Float


class InitializeWorldBorder(Packet, kw_only=True):
    """Packet representing InitializeWorldBorder."""

    __packet_name__: ClassVar[str] = "play:clientbound:initialize_world_border"

    x: Double
    z: Double
    old_diameter: Double
    new_diameter: Double
    speed: VarInt
    portal_teleport_boundary: VarInt
    warning_blocks: VarInt
    warning_time: VarInt


class KeepAlive(Packet, kw_only=True):
    """Packet representing KeepAlive."""

    __packet_name__: ClassVar[str] = "play:clientbound:keep_alive"

    keep_alive_id: Long


class MapChunk(Packet, kw_only=True):
    """Packet representing MapChunk."""

    __packet_name__: ClassVar[str] = "play:clientbound:map_chunk"

    x: Int
    z: Int
    heightmaps: HeightmapsArray
    chunk_data: ByteArray
    block_entities: BlockEntityArray
    sky_light_mask: LongArray
    block_light_mask: LongArray
    empty_sky_light_mask: LongArray
    empty_block_light_mask: LongArray
    sky_light: LightData
    block_light: LightData


class WorldEvent(Packet, kw_only=True):
    """Packet representing WorldEvent."""

    __packet_name__: ClassVar[str] = "play:clientbound:world_event"

    effect_id: Int
    location: PositionType
    data: Int
    global_: Boolean


class WorldParticles(Packet, kw_only=True):
    """Packet representing WorldParticles."""

    __packet_name__: ClassVar[str] = "play:clientbound:world_particles"

    long_distance: Boolean
    always_show: Boolean
    x: Double
    y: Double
    z: Double

    offset_x: Float
    offset_y: Float
    offset_z: Float

    velocity_offset: Float
    amount: Int
    particle: ParticleData


class UpdateLight(Packet, kw_only=True):
    """Packet representing UpdateLight."""

    __packet_name__: ClassVar[str] = "play:clientbound:update_light"

    chunk_x: VarInt
    chunk_z: VarInt
    sky_light_mask: LongArray
    block_light_mask: LongArray
    empty_sky_light_mask: LongArray
    empty_block_light_mask: LongArray
    sky_light: Light
    block_light: Light


class Login(Packet, kw_only=True):
    """Packet representing Login."""

    __packet_name__: ClassVar[str] = "play:clientbound:login"

    entity_id: Int
    is_hardcore: Boolean

    world_names: IdentifierArray

    max_players: VarInt
    view_distance: VarInt
    simulation_distance: VarInt
    reduced_debug_info: Boolean
    enable_respawn_screen: Boolean
    do_limited_crafting: Boolean

    world_state: WorldState

    enforces_secure_chat: Boolean


class Map(Packet, kw_only=True):
    """Packet representing Map."""

    __packet_name__: ClassVar[str] = "play:clientbound:map"

    map_id: VarInt
    scale: Byte
    locked: Boolean
    icons: OptionalMapIconArray
    color_patch: MapColorPatch


class TradeList(Packet, kw_only=True):
    """Packet representing TradeList."""

    __packet_name__: ClassVar[str] = "play:clientbound:trade_list"

    window_id: VarInt
    trades: TradeArray
    villager_level: VarInt
    experience: VarInt
    is_regular_villager: Boolean
    can_restock: Boolean


class RelEntityMove(Packet, kw_only=True):
    """Packet representing RelEntityMove."""

    __packet_name__: ClassVar[str] = "play:clientbound:rel_entity_move"

    entity_id: VarInt
    d_x: Short
    d_y: Short
    d_z: Short
    on_ground: Boolean


class EntityMoveLook(Packet, kw_only=True):
    """Packet representing EntityMoveLook."""

    __packet_name__: ClassVar[str] = "play:clientbound:entity_move_look"

    entity_id: VarInt
    d_x: Short
    d_y: Short
    d_z: Short
    yaw: Byte
    pitch: Byte
    on_ground: Boolean


class MoveMinecart(Packet, kw_only=True):
    """Packet representing MoveMinecart."""

    __packet_name__: ClassVar[str] = "play:clientbound:move_minecart"

    entity_id: VarInt
    steps: MinecartStepArray


class EntityLook(Packet, kw_only=True):
    """Packet representing EntityLook."""

    __packet_name__: ClassVar[str] = "play:clientbound:entity_look"

    entity_id: VarInt
    yaw: Byte
    pitch: Byte
    on_ground: Boolean


class VehicleMove(Packet, kw_only=True):
    """Packet representing VehicleMove."""

    __packet_name__: ClassVar[str] = "play:clientbound:vehicle_move"

    x: Double
    y: Double
    z: Double
    yaw: Float
    pitch: Float


class OpenBook(Packet, kw_only=True):
    """Packet representing OpenBook."""

    __packet_name__: ClassVar[str] = "play:clientbound:open_book"

    hand: VarInt


class OpenWindow(Packet, kw_only=True):
    """Packet representing OpenWindow."""

    __packet_name__: ClassVar[str] = "play:clientbound:open_window"

    window_id: VarInt
    inventory_type: VarInt
    window_title: NBTCompound


class OpenSignEntity(Packet, kw_only=True):
    """Packet representing OpenSignEntity."""

    __packet_name__: ClassVar[str] = "play:clientbound:open_sign_entity"

    location: PositionType

    is_front_text: Boolean


class Ping(Packet, kw_only=True):
    """Packet representing Ping."""

    __packet_name__: ClassVar[str] = "play:clientbound:ping"

    id_: Int


class PingResponse(Packet, kw_only=True):
    """Packet representing PingResponse."""

    __packet_name__: ClassVar[str] = "play:clientbound:ping_response"

    id_: Long


class CraftRecipeResponse(Packet, kw_only=True):
    """Packet representing CraftRecipeResponse."""

    __packet_name__: ClassVar[str] = "play:clientbound:craft_recipe_response"

    window_id: VarInt
    recipe_display: RecipeDisplay


class Abilities(Packet, kw_only=True):
    """Packet representing Abilities."""

    __packet_name__: ClassVar[str] = "play:clientbound:abilities"

    flags: Byte
    flying_speed: Float
    walking_speed: Float


class PlayerChat(Packet, kw_only=True):
    """Packet representing PlayerChat."""

    __packet_name__: ClassVar[str] = "play:clientbound:player_chat"

    global_index: VarInt
    sender_uuid: UUID
    index: VarInt
    signature: OptionalByteArray
    plain_message: String
    timestamp: Long
    salt: Long
    previous_messages: MessageSignatureArray
    filter_type: VarInt
    filter_type_mask: OptionalBitSet
    type_: ChatType
    network_name: TextComponent
    network_target_name: TextComponent


class EndCombatEvent(Packet, kw_only=True):
    """Packet representing EndCombatEvent."""

    __packet_name__: ClassVar[str] = "play:clientbound:end_combat_event"

    duration: VarInt


class EnterCombatEvent(Packet, kw_only=True):
    """Packet representing EnterCombatEvent."""

    __packet_name__: ClassVar[str] = "play:clientbound:enter_combat_event"


class DeathCombatEvent(Packet, kw_only=True):
    """Packet representing DeathCombatEvent."""

    __packet_name__: ClassVar[str] = "play:clientbound:death_combat_event"

    player_id: VarInt
    message: NBTCompound


class PlayerRemove(Packet, kw_only=True):
    """Packet representing PlayerRemove."""

    __packet_name__: ClassVar[str] = "play:clientbound:player_remove"

    players: UUIDArray


class PlayerInfo(Packet, kw_only=True):
    """Packet representing PlayerInfo."""

    __packet_name__: ClassVar[str] = "play:clientbound:player_info"

    player_info: PlayerInfoUpdateData


class FacePlayer(Packet, kw_only=True):
    """Packet representing FacePlayer."""

    __packet_name__: ClassVar[str] = "play:clientbound:face_player"

    feet_eyes: VarInt
    x: Double
    y: Double
    z: Double
    is_entity: Boolean
    entity_id: OptionalVarInt
    entity_feet_eyes: VarInt  # TODO(IvanPythonov): Look at VarInt enum


class Position(Packet, kw_only=True):
    """Packet representing Position."""

    __packet_name__: ClassVar[str] = "play:clientbound:position"

    teleport_id: VarInt
    x: Double
    y: Double
    z: Double
    dx: Double
    dy: Double
    dz: Double
    yaw: Float
    pitch: Float
    flags: TeleportFlags


class PlayerRotation(Packet, kw_only=True):
    """Packet representing PlayerRotation."""

    __packet_name__: ClassVar[str] = "play:clientbound:player_rotation"

    yaw: Float
    pitch: Float


class RecipeBookAdd(Packet, kw_only=True):
    """Packet representing RecipeBookAdd."""

    __packet_name__: ClassVar[str] = "play:clientbound:recipe_book_add"

    entries: Recipe
    replace: Boolean


class RecipeBookRemove(Packet, kw_only=True):
    """Packet representing RecipeBookRemove."""

    __packet_name__: ClassVar[str] = "play:clientbound:recipe_book_remove"

    recipe_ids: VarIntArray


class RecipeBookSettings(Packet, kw_only=True):
    """Packet representing RecipeBookSettings."""

    __packet_name__: ClassVar[str] = "play:clientbound:recipe_book_settings"

    crafting_recipe_book_open: Boolean
    crafting_recipe_book_filter_active: Boolean

    smelting_recipe_book_open: Boolean
    smelting_recipe_book_filter_active: Boolean

    smoker_recipe_book_open: Boolean
    smoker_recipe_book_filter_active: Boolean


class EntityDestroy(Packet, kw_only=True):
    """Packet representing EntityDestroy."""

    __packet_name__: ClassVar[str] = "play:clientbound:entity_destroy"

    entity_ids: VarIntArray


class RemoveEntityEffect(Packet, kw_only=True):
    """Packet representing RemoveEntityEffect."""

    __packet_name__: ClassVar[str] = "play:clientbound:remove_entity_effect"

    entity_id: VarInt
    effect_id: VarInt


class ResetScore(Packet, kw_only=True):
    """Packet representing ResetScore."""

    __packet_name__: ClassVar[str] = "play:clientbound:reset_score"

    entity_name: String
    objective_name: OptionalString


class RemoveResourcePack(Packet, kw_only=True):
    """Packet representing RemoveResourcePack."""

    __packet_name__: ClassVar[str] = "play:clientbound:remove_resource_pack"


class AddResourcePack(Packet, kw_only=True):
    """Packet representing AddResourcePack."""

    __packet_name__: ClassVar[str] = "play:clientbound:add_resource_pack"


class Respawn(Packet, kw_only=True):
    """Packet representing Respawn."""

    __packet_name__: ClassVar[str] = "play:clientbound:respawn"

    world_state: WorldState

    copy_metadata: UByte


class EntityHeadRotation(Packet, kw_only=True):
    """Packet representing EntityHeadRotation."""

    __packet_name__: ClassVar[str] = "play:clientbound:entity_head_rotation"

    entity_id: VarInt
    head_yaw: Byte


class MultiBlockChange(Packet, kw_only=True):
    """Packet representing MultiBlockChange."""

    __packet_name__: ClassVar[str] = "play:clientbound:multi_block_change"

    chunk_coordinates: Byte
    records: VarIntArray


class SelectAdvancementTab(Packet, kw_only=True):
    """Packet representing SelectAdvancementTab."""

    __packet_name__: ClassVar[str] = "play:clientbound:select_advancement_tab"

    id_: OptionalIdentifier

    # !minecraft:story/root
    # !minecraft:nether/root
    # !minecraft:end/root
    # !minecraft:adventure/root
    # !minecraft:husbandry/root

    # TODO(IvanPythonov): ENUMS


class ServerData(Packet, kw_only=True):
    """Packet representing ServerData."""

    __packet_name__: ClassVar[str] = "play:clientbound:server_data"

    motd: TextComponent
    icon_bytes: OptionalByteArray


class ActionBar(Packet, kw_only=True):
    """Packet representing ActionBar."""

    __packet_name__: ClassVar[str] = "play:clientbound:action_bar"

    text: TextComponent


class WorldBorderCenter(Packet, kw_only=True):
    """Packet representing WorldBorderCenter."""

    __packet_name__: ClassVar[str] = "play:clientbound:world_border_center"

    x: Double
    z: Double


class WorldBorderLerpSize(Packet, kw_only=True):
    """Packet representing WorldBorderLerpSize."""

    __packet_name__: ClassVar[str] = "play:clientbound:world_border_lerp_size"

    old_diameter: Double
    new_diameter: Double
    speed: VarInt


class WorldBorderSize(Packet, kw_only=True):
    """Packet representing WorldBorderSize."""

    __packet_name__: ClassVar[str] = "play:clientbound:world_border_size"

    diameter: Double


class WorldBorderWarningDelay(Packet, kw_only=True):
    """Packet representing WorldBorderWarningDelay."""

    __packet_name__: ClassVar[str] = (
        "play:clientbound:world_border_warning_delay"
    )

    warning_time: VarInt


class WorldBorderWarningReach(Packet, kw_only=True):
    """Packet representing WorldBorderWarningReach."""

    __packet_name__: ClassVar[str] = (
        "play:clientbound:world_border_warning_reach"
    )

    warning_blocks: VarInt


class Camera(Packet, kw_only=True):
    """Packet representing Camera."""

    __packet_name__: ClassVar[str] = "play:clientbound:camera"

    camera_id: VarInt


class UpdateViewPosition(Packet, kw_only=True):
    """Packet representing UpdateViewPosition."""

    __packet_name__: ClassVar[str] = "play:clientbound:update_view_position"

    chunk_x: VarInt
    chunk_z: VarInt


class UpdateViewDistance(Packet, kw_only=True):
    """Packet representing UpdateViewDistance."""

    __packet_name__: ClassVar[str] = "play:clientbound:update_view_distance"

    view_distance: VarInt


class SetCursorItem(Packet, kw_only=True):
    """Packet representing SetCursorItem."""

    __packet_name__: ClassVar[str] = "play:clientbound:set_cursor_item"

    contents: Slot


class SpawnPosition(Packet, kw_only=True):
    """Packet representing SpawnPosition."""

    __packet_name__: ClassVar[str] = "play:clientbound:spawn_position"

    location: PositionType
    angle: Float


class ScoreboardDisplayObjective(Packet, kw_only=True):
    """Packet representing ScoreboardDisplayObjective."""

    __packet_name__: ClassVar[str] = (
        "play:clientbound:scoreboard_display_objective"
    )

    position: VarInt
    name: String


class EntityMetadata(Packet, kw_only=True):
    """Packet representing EntityMetadata."""

    __packet_name__: ClassVar[str] = "play:clientbound:entity_metadata"

    entity_id: VarInt
    metadata: RestBuffer  # TODO(IvanPythonov): suka...


class AttachEntity(Packet, kw_only=True):
    """Packet representing AttachEntity."""

    __packet_name__: ClassVar[str] = "play:clientbound:attach_entity"

    entity_id: Int
    vehicle_id: Int


class EntityVelocity(Packet, kw_only=True):
    """Packet representing EntityVelocity."""

    __packet_name__: ClassVar[str] = "play:clientbound:entity_velocity"

    entity_id: VarInt
    velocity_x: Short
    velocity_y: Short
    velocity_z: Short


class EntityEquipment(Packet, kw_only=True):
    """Packet representing EntityEquipment."""

    __packet_name__: ClassVar[str] = "play:clientbound:entity_equipment"

    entity_id: VarInt
    equipment: EquipmentArray


class Experience(Packet, kw_only=True):
    """Packet representing Experience."""

    __packet_name__: ClassVar[str] = "play:clientbound:experience"

    experience_bar: Float
    level: VarInt
    total_experience: VarInt


class UpdateHealth(Packet, kw_only=True):
    """Packet representing UpdateHealth."""

    __packet_name__: ClassVar[str] = "play:clientbound:update_health"

    health: Float
    food: VarInt
    food_saturation: Float


class HeldItemSlot(Packet, kw_only=True):
    """Packet representing HeldItemSlot."""

    __packet_name__: ClassVar[str] = "play:clientbound:held_item_slot"

    slot: VarInt


class ScoreboardObjective(Packet, kw_only=True):
    """Packet representing ScoreboardObjective."""

    __packet_name__: ClassVar[str] = "play:clientbound:scoreboard_objective"

    objective_data: UpdateObjectiveData


class SetPassengers(Packet, kw_only=True):
    """Packet representing SetPassengers."""

    __packet_name__: ClassVar[str] = "play:clientbound:set_passengers"

    entity_id: VarInt
    passengers: VarIntArray


class SetPlayerInventory(Packet, kw_only=True):
    """Packet representing SetPlayerInventory."""

    __packet_name__: ClassVar[str] = "play:clientbound:set_player_inventory"

    slot_id: VarInt
    contents: Slot


class Teams(Packet, kw_only=True):
    """Packet representing Teams."""

    __packet_name__: ClassVar[str] = "play:clientbound:teams"

    team_data: UpdateTeamData


class ScoreboardScore(Packet, kw_only=True):
    """Packet representing ScoreboardScore."""

    __packet_name__: ClassVar[str] = "play:clientbound:scoreboard_score"

    entity_name: String
    objective_name: String
    value: VarInt
    display_name: PrefixedOptionalTextComponent
    number_format: PrefixedOptionalNumberFormat


class SimulationDistance(Packet, kw_only=True):
    """Packet representing SimulationDistance."""

    __packet_name__: ClassVar[str] = "play:clientbound:simulation_distance"

    distance: VarInt


class SetTitleSubtitle(Packet, kw_only=True):
    """Packet representing SetTitleSubtitle."""

    __packet_name__: ClassVar[str] = "play:clientbound:set_title_subtitle"

    text: NBTCompound


class UpdateTime(Packet, kw_only=True):
    """Packet representing UpdateTime."""

    __packet_name__: ClassVar[str] = "play:clientbound:update_time"

    age: Long
    time: Long
    tick_day_time: Boolean


class SetTitleText(Packet, kw_only=True):
    """Packet representing SetTitleText."""

    __packet_name__: ClassVar[str] = "play:clientbound:set_title_text"

    text: NBTCompound


class SetTitleTime(Packet, kw_only=True):
    """Packet representing SetTitleTime."""

    __packet_name__: ClassVar[str] = "play:clientbound:set_title_time"

    fade_in: Int
    stay: Int
    fade_out: Int


class EntitySoundEffect(Packet, kw_only=True):
    """Packet representing EntitySoundEffect."""

    __packet_name__: ClassVar[str] = "play:clientbound:entity_sound_effect"

    sound_event: SoundEvent
    sound_category: VarInt

    entity_id: VarInt
    volume: Float
    pitch: Float
    seed: Long


class SoundEffect(Packet, kw_only=True):
    """Packet representing SoundEffect."""

    __packet_name__: ClassVar[str] = "play:clientbound:sound_effect"

    sound_event: SoundEvent
    sound_category: VarInt

    effect_position_x: Int
    effect_position_y: Int
    effect_position_z: Int

    volume: Float
    pitch: Float
    seed: Long


class StartConfiguration(Packet, kw_only=True):
    """Packet representing StartConfiguration."""

    __packet_name__: ClassVar[str] = "play:clientbound:start_configuration"


class StopSound(Packet, kw_only=True):
    """Packet representing StopSound."""

    __packet_name__: ClassVar[str] = "play:clientbound:stop_sound"

    flags: Byte

    source: OptionalVarInt
    sound: OptionalIdentifier


class StoreCookie(Packet, kw_only=True):
    """Packet representing StoreCookie."""

    __packet_name__: ClassVar[str] = "play:clientbound:store_cookie"


class SystemChat(Packet, kw_only=True):
    """Packet representing SystemChat."""

    __packet_name__: ClassVar[str] = "play:clientbound:system_chat"

    content: NBTCompound
    is_action_bar: Boolean


class PlayerlistHeader(Packet, kw_only=True):
    """Packet representing PlayerlistHeader."""

    __packet_name__: ClassVar[str] = "play:clientbound:playerlist_header"

    header: NBTCompound
    footer: NBTCompound


class NbtQueryResponse(Packet, kw_only=True):
    """Packet representing NbtQueryResponse."""

    __packet_name__: ClassVar[str] = "play:clientbound:nbt_query_response"

    transaction_id: VarInt
    nbt: NBTCompound | None


class Collect(Packet, kw_only=True):
    """Packet representing Collect."""

    __packet_name__: ClassVar[str] = "play:clientbound:collect"

    collected_entity_id: VarInt
    collector_entity_id: VarInt
    pickup_item_count: VarInt


class EntityTeleport(Packet, kw_only=True):
    """Packet representing EntityTeleport."""

    __packet_name__: ClassVar[str] = "play:clientbound:entity_teleport"

    entity_id: VarInt
    x: Double
    y: Double
    z: Double
    yaw: Byte
    pitch: Byte
    on_ground: Boolean


class TestInstanceBlockStatus(Packet, kw_only=True):
    """Packet representing TestInstanceBlockStatus."""

    __packet_name__: ClassVar[str] = (
        "play:clientbound:test_instance_block_status"
    )

    status: NBTCompound

    has_size: Boolean

    size_x: OptionalDouble
    size_y: OptionalDouble
    size_z: OptionalDouble


class SetTickingState(Packet, kw_only=True):
    """Packet representing SetTickingState."""

    __packet_name__: ClassVar[str] = "play:clientbound:set_ticking_state"

    tick_rate: Float
    is_frozen: Boolean


class StepTick(Packet, kw_only=True):
    """Packet representing StepTick."""

    __packet_name__: ClassVar[str] = "play:clientbound:step_tick"

    tick_steps: VarInt


class Transfer(Packet, kw_only=True):
    """Packet representing Transfer."""

    __packet_name__: ClassVar[str] = "play:clientbound:transfer"


class Advancements(Packet, kw_only=True):
    """Packet representing Advancements."""

    __packet_name__: ClassVar[str] = "play:clientbound:advancements"

    reset_clear: Boolean
    advancement_mapping: AdvancementMappingArray
    identifiers: IdentifierArray
    progress_mapping: ProgressMappingArray
    show_advancements: Boolean


class EntityUpdateAttributes(Packet, kw_only=True):
    """Packet representing EntityUpdateAttributes."""

    __packet_name__: ClassVar[str] = (
        "play:clientbound:entity_update_attributes"
    )

    entity_id: VarInt
    properties: AttributePropertyArray


class EntityEffect(Packet, kw_only=True):
    """Packet representing EntityEffect."""

    __packet_name__: ClassVar[str] = "play:clientbound:entity_effect"

    entity_id: VarInt
    effect_id: VarInt
    amplifier: VarInt
    duration: VarInt
    flags: UByte


class DeclareRecipes(Packet, kw_only=True):
    """Packet representing DeclareRecipes."""

    __packet_name__: ClassVar[str] = "play:clientbound:declare_recipes"

    property_sets: PropertySetArray
    stonecutter_recipes: StonecutterRecipeArray


class Tags(Packet, kw_only=True):
    """Packet representing Tags."""

    __packet_name__: ClassVar[str] = "play:clientbound:tags"

    tags: IdentifierArray


class SetProjectilePower(Packet, kw_only=True):
    """Packet representing SetProjectilePower."""

    __packet_name__: ClassVar[str] = "play:clientbound:set_projectile_power"

    id_: VarInt
    acceleration_power: Double


class CustomReportDetails(Packet, kw_only=True):
    """Packet representing CustomReportDetails."""

    __packet_name__: ClassVar[str] = "play:clientbound:custom_report_details"


class ServerLinks(Packet, kw_only=True):
    """Packet representing ServerLinks."""

    __packet_name__: ClassVar[str] = "play:clientbound:server_links"


class TrackedWaypoint(Packet, kw_only=True):
    """Packet representing TrackedWaypoint."""

    __packet_name__: ClassVar[str] = "play:clientbound:tracked_waypoint"

    operation: VarInt
    identifier: String
    icon_style: Identifier
    color: PrefixedOptionalWaypointColor
    waypoint_data: WaypointData


class ClearDialog(Packet, kw_only=True):
    """Packet representing ClearDialog."""

    __packet_name__: ClassVar[str] = "play:clientbound:clear_dialog"


class ShowDialog(Packet, kw_only=True):
    """Packet representing ShowDialog."""

    __packet_name__: ClassVar[str] = "play:clientbound:show_dialog"

    dialog: VarInt
