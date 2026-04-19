from typing import Annotated

from nbtlib import Base as BaseTag

from pythonium.engine.codecs import (
    BooleanCodec,
    ByteCodec,
    DoubleCodec,
    FloatCodec,
    IntCodec,
    LongCodec,
    NBTCodec,
    PositionCodec,
    ShortCodec,
    StringCodec,
    UnsignedByteCodec,
    UnsignedShortCodec,
    UUIDCodec,
    VarIntCodec,
    VarLongCodec,
)
from pythonium.engine.codecs.advancement import (
    AdvancementMappingCodec,
    AdvancementMappingStruct,
    ProgressMappingCodec,
    ProgressMappingStruct,
)
from pythonium.engine.codecs.array import ArrayCodec
from pythonium.engine.codecs.attributes import (
    AttributePropertyCodec,
    AttributePropertyStruct,
)
from pythonium.engine.codecs.bitset import BitSetCodec
from pythonium.engine.codecs.boss_bar_action import (
    BossBarAction,
    BossBarActionCodec,
)
from pythonium.engine.codecs.chat_codecs import (
    ArgumentSignatureCodec,
    ArgumentSignatureStruct,
    MessageSignatureCodec,
    MessageSignatureStruct,
)
from pythonium.engine.codecs.chat_type import ChatTypeCodec, ChatTypeStruct
from pythonium.engine.codecs.chunk import (
    BlockEntityCodec,
    BlockEntityStruct,
    ChunkBiomeDataCodec,
    ChunkBiomeDataStruct,
    HeightmapsCodec,
    LightDataCodec,
    LightDataStruct,
)
from pythonium.engine.codecs.commands import (
    CommandMatchCodec,
    CommandMatchStruct,
)
from pythonium.engine.codecs.custom import (
    DoubleVectorCodec,
    FixedByteArrayCodec,
    JsonTextComponentCodec,
    PrefixedByteArrayCodec,
    PrefixedLongByteArrayCodec,
    TextComponentCodec,
)
from pythonium.engine.codecs.equipment import (
    EquipmentArrayCodec,
    EquipmentEntryStruct,
)
from pythonium.engine.codecs.game_codecs import (
    ModifierDataCodec,
    ModifierDataStruct,
)
from pythonium.engine.codecs.identifier import IdentifierCodec
from pythonium.engine.codecs.map_data import (
    MapColorPatchCodec,
    MapColorPatchStruct,
    MapIconCodec,
    MapIconStruct,
)
from pythonium.engine.codecs.minecart import (
    MinecartStepCodec,
    MinecartStepStruct,
)
from pythonium.engine.codecs.node import NodeCodec, NodeStruct
from pythonium.engine.codecs.optional import OptionalCodec
from pythonium.engine.codecs.particle import (
    BlockParticleAlternativeCodec,
    BlockParticleAlternativeStruct,
    ParticleDataCodec,
    ParticleDataStruct,
)
from pythonium.engine.codecs.player_info import (
    PlayerInfoUpdateCodec,
    PlayerInfoUpdateStruct,
)
from pythonium.engine.codecs.recipe import (
    RecipeCodec,
    RecipeDisplayCodec,
    RecipeDisplayStruct,
    RecipeStruct,
)
from pythonium.engine.codecs.rest_buffer import RestBufferCodec
from pythonium.engine.codecs.scoreboard import (
    NumberFormatCodec,
    NumberFormatStruct,
    UpdateObjectiveCodec,
    UpdateObjectiveStruct,
)
from pythonium.engine.codecs.slot import (
    ChangedSlotCodec,
    ChangedSlotStruct,
    HashedSlotCodec,
    HashedSlotStruct,
    SlotCodec,
    SlotStruct,
)
from pythonium.engine.codecs.sound_event import (
    SoundEventCodec,
    SoundEventStruct,
)
from pythonium.engine.codecs.statistics import StatisticCodec, StatisticStruct
from pythonium.engine.codecs.tag import RegistryTagsCodec, RegistryTagsStruct
from pythonium.engine.codecs.teams import UpdateTeamCodec, UpdateTeamStruct
from pythonium.engine.codecs.trade import TradeCodec, TradeStruct
from pythonium.engine.codecs.update_recipes import (
    PropertySetCodec,
    PropertySetStruct,
    StonecutterRecipeCodec,
    StonecutterRecipeStruct,
)
from pythonium.engine.codecs.waypoint import (
    WaypointColorCodec,
    WaypointColorStruct,
    WaypointDataCodec,
    WaypointDataStruct,
)
from pythonium.engine.codecs.world import WorldStateCodec, WorldStateStruct

type VarInt = Annotated[int, VarIntCodec()]
type VarLong = Annotated[int, VarLongCodec()]

type Byte = Annotated[int, ByteCodec()]
type UByte = Annotated[int, UnsignedByteCodec()]

type Short = Annotated[int, ShortCodec()]
type UShort = Annotated[int, UnsignedShortCodec()]

type Int = Annotated[int, IntCodec()]
type Long = Annotated[int, LongCodec()]

type Float = Annotated[float, FloatCodec()]
type Double = Annotated[float, DoubleCodec()]

type String = Annotated[str, StringCodec()]
type UUID = Annotated[str, UUIDCodec()]
type Boolean = Annotated[bool, BooleanCodec()]

type Position = Annotated[tuple[int, int, int], PositionCodec()]

type ByteArray = Annotated[list[int], ArrayCodec(ByteCodec())]
type UByteArray = Annotated[list[int], ArrayCodec(UnsignedByteCodec())]

type ShortArray = Annotated[list[int], ArrayCodec(ShortCodec())]
type UShortArray = Annotated[list[int], ArrayCodec(UnsignedShortCodec())]

type IntArray = Annotated[list[int], ArrayCodec(IntCodec())]
type LongArray = Annotated[list[int], ArrayCodec(LongCodec())]

type FloatArray = Annotated[list[float], ArrayCodec(FloatCodec())]
type DoubleArray = Annotated[list[float], ArrayCodec(DoubleCodec())]

type StringArray = Annotated[list[str], ArrayCodec(StringCodec())]
type UUIDArray = Annotated[list[str], ArrayCodec(UUIDCodec())]
type BooleanArray = Annotated[list[bool], ArrayCodec(BooleanCodec())]

type VarIntArray = Annotated[list[int], ArrayCodec(VarIntCodec())]
type VarLongArray = Annotated[list[int], ArrayCodec(VarLongCodec())]

type OptionalString = Annotated[str | None, OptionalCodec(StringCodec())]
type OptionalVarInt = Annotated[int | None, OptionalCodec(VarIntCodec())]
type OptionalUUID = Annotated[str | None, OptionalCodec(UUIDCodec())]
type OptionalBoolean = Annotated[bool | None, OptionalCodec(BooleanCodec())]
type OptionalPosition = Annotated[
    tuple[int, int, int] | None, OptionalCodec(PositionCodec())
]
type OptionalNBT = Annotated[
    dict[str, BaseTag] | None, OptionalCodec(NBTCodec())
]
type OptionalFloat = Annotated[float | None, OptionalCodec(FloatCodec())]
type OptionalDouble = Annotated[float | None, OptionalCodec(DoubleCodec())]

type NBTCompound = Annotated[dict[str, BaseTag], NBTCodec()]

type Identifier = Annotated[str, IdentifierCodec()]
type IdentifierArray = Annotated[list[str], ArrayCodec(StringCodec())]

type TextComponent = Annotated[NBTCompound, TextComponentCodec()]
type ModifierData = Annotated[ModifierDataStruct, ModifierDataCodec()]

type JsonTextComponent = Annotated[str, JsonTextComponentCodec()]
type Slot = Annotated[SlotStruct, SlotCodec()]

type SlotArray = Annotated[list[SlotStruct], ArrayCodec(SlotCodec())]

type Recipe = Annotated[RecipeStruct, RecipeCodec()]
type RecipeArray = Annotated[list[RecipeStruct], ArrayCodec(RecipeCodec())]

type OptionalByteArray = Annotated[
    ByteArray | None, OptionalCodec(ArrayCodec(ByteCodec()))
]

type MessageSignature = Annotated[
    MessageSignatureStruct, MessageSignatureCodec()
]

type MessageSignatureArray = Annotated[
    list[MessageSignatureStruct], ArrayCodec(MessageSignatureCodec())
]

type RecipeDisplay = Annotated[RecipeDisplayStruct, RecipeDisplayCodec()]
type RecipeDisplayArray = Annotated[
    list[RecipeDisplayStruct], ArrayCodec(RecipeDisplayCodec())
]

type TradeArray = Annotated[list[TradeStruct], ArrayCodec(TradeCodec())]

type OptionalMapIconArray = Annotated[
    list[MapIconStruct] | None, OptionalCodec(ArrayCodec(MapIconCodec()))
]
type MapColorPatch = Annotated[MapColorPatchStruct, MapColorPatchCodec()]

type MinecartStepArray = Annotated[
    list[MinecartStepStruct], ArrayCodec(MinecartStepCodec())
]
type PrefixedLongByteArray = Annotated[bytes, PrefixedLongByteArrayCodec()]

type BossBarActionType = Annotated[BossBarAction, BossBarActionCodec()]

type RestBuffer = Annotated[bytes, RestBufferCodec()]

type PrefixedOptionalTextComponent = Annotated[
    NBTCompound | None, OptionalCodec(TextComponentCodec())
]
type OptionalIdentifier = Annotated[str | None, OptionalCodec(StringCodec())]


type BitSet = Annotated[list[int], BitSetCodec()]
type OptionalBitSet = Annotated[list[int] | None, OptionalCodec(BitSetCodec())]

type AttributePropertyArray = Annotated[
    list[AttributePropertyStruct], ArrayCodec(AttributePropertyCodec())
]

type PropertySetArray = Annotated[
    list[PropertySetStruct], ArrayCodec(PropertySetCodec())
]
type StonecutterRecipeArray = Annotated[
    list[StonecutterRecipeStruct], ArrayCodec(StonecutterRecipeCodec())
]

type SoundEvent = Annotated[SoundEventStruct, SoundEventCodec()]

type WorldState = Annotated[WorldStateStruct, WorldStateCodec()]

type Light = Annotated[
    list[list[UByte]], ArrayCodec(ArrayCodec(UnsignedByteCodec()))
]


type HashedSlot = Annotated[HashedSlotStruct, HashedSlotCodec()]

type ChangedSlotArray = Annotated[
    list[ChangedSlotStruct], ArrayCodec(ChangedSlotCodec())
]

type ArgumentSignatureArray = Annotated[
    list[ArgumentSignatureStruct], ArrayCodec(ArgumentSignatureCodec())
]

type FixedBitSet20 = Annotated[
    bytes, FixedByteArrayCodec(3)
]  # ceil(20 / 8) bytes = 3 bytes

type CommandMatchArray = Annotated[
    list[CommandMatchStruct], ArrayCodec(CommandMatchCodec())
]

type ChunkBiomeDataArray = Annotated[
    list[ChunkBiomeDataStruct], ArrayCodec(ChunkBiomeDataCodec())
]

type StatisticArray = Annotated[
    list[StatisticStruct], ArrayCodec(StatisticCodec())
]

type ChatType = Annotated[ChatTypeStruct, ChatTypeCodec()]

type OptionalDoubleVector = Annotated[
    tuple[float, float, float] | None, OptionalCodec(DoubleVectorCodec())
]

type ParticleData = Annotated[ParticleDataStruct, ParticleDataCodec()]
type BlockParticleAlternativeArray = Annotated[
    list[BlockParticleAlternativeStruct],
    ArrayCodec(BlockParticleAlternativeCodec()),
]
type PrefixedByteArray = Annotated[bytes, PrefixedByteArrayCodec()]

type BlockEntityArray = Annotated[
    list[BlockEntityStruct], ArrayCodec(BlockEntityCodec())
]
type LightData = Annotated[LightDataStruct, LightDataCodec()]

type PrefixedOptionalWaypointColor = Annotated[
    WaypointColorStruct | None, OptionalCodec(WaypointColorCodec())
]
type WaypointData = Annotated[WaypointDataStruct, WaypointDataCodec()]

type PrefixedOptionalNumberFormat = Annotated[
    NumberFormatStruct | None, OptionalCodec(NumberFormatCodec())
]

type AdvancementMappingArray = Annotated[
    list[AdvancementMappingStruct], ArrayCodec(AdvancementMappingCodec())
]
type ProgressMappingArray = Annotated[
    list[ProgressMappingStruct], ArrayCodec(ProgressMappingCodec())
]

type UpdateObjectiveData = Annotated[
    UpdateObjectiveStruct, UpdateObjectiveCodec()
]
type EquipmentArray = Annotated[
    list[EquipmentEntryStruct], EquipmentArrayCodec()
]
type UpdateTeamData = Annotated[UpdateTeamStruct, UpdateTeamCodec()]


type PlayerInfoUpdateData = Annotated[
    PlayerInfoUpdateStruct, PlayerInfoUpdateCodec()
]

type TagArray = Annotated[
    list[RegistryTagsStruct], ArrayCodec(RegistryTagsCodec())
]

type HeightmapData = Annotated[dict[str, list[int]], HeightmapsCodec()]

type NodeArray = Annotated[list[NodeStruct], ArrayCodec(NodeCodec())]
