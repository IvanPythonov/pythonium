"""Configuration Phase Router."""

import asyncio
import hashlib
import secrets
from logging import getLogger

from pythonium.engine import Client, Router
from pythonium.engine.codecs.player_info import (
    PlayerInfoActionStruct,
    PlayerInfoUpdateStruct,
)
from pythonium.engine.codecs.world import WorldStateStruct
from pythonium.engine.enums import State
from pythonium.engine.enums.abilities import AbilitiesFlags
from pythonium.engine.enums.teleport_flags import TeleportFlags
from pythonium.engine.exceptions import ImpossibleError, SuspiciousClientError
from pythonium.engine.packets.ingoing.configuration import (
    CustomPayload,
    Pong,
    Settings,
)
from pythonium.engine.packets.ingoing.configuration import (
    FinishConfiguration as FinishConfigurationRequest,
)
from pythonium.engine.packets.ingoing.configuration import (
    KeepAlive as KeepAliveRequest,
)
from pythonium.engine.packets.outgoing import UpdateViewDistance
from pythonium.engine.packets.outgoing.configuration import (
    FeatureFlags,
    Ping,
    Tags,
)
from pythonium.engine.packets.outgoing.configuration import (
    FinishConfiguration as FinishConfigurationAcknowledge,
)
from pythonium.engine.packets.outgoing.configuration import (
    KeepAlive as KeepAliveResponse,
)
from pythonium.engine.packets.outgoing.play import (
    Abilities,
    Difficulty,
    EntityStatus,
    GameStateChange,
    HeldItemSlot,
    Login,
    PlayerInfo,
    Position,
    SetTickingState,
    SpawnPosition,
    UpdateViewPosition,
)
from pythonium.engine.properties_reader import Properties
from pythonium.engine.ticker.ticker import Ticker
from pythonium.engine.world import World
from pythonium.registries.registries_storage import REGISTRY_REGISTRY
from pythonium.worldgen.chunk_sender import ChunkSender

logger = getLogger(__name__)
router = Router(name=__name__)


def _seed_hash(seed: int) -> int:
    """
    Generate a hashed seed.

    First 8 bytes of the SHA-256 hash of the world's seed.
    Used client-side for biome noise.
    """
    return int.from_bytes(
        hashlib.sha256(seed.to_bytes(8, "big")).digest()[:8],
        "big",
        signed=False,
    )


@router.registry(Settings)
async def on_settings_registry(
    packet: Settings,
) -> None:
    return REGISTRY_REGISTRY.values()


@router.on(Settings)
async def on_client_information(
    client_information: Settings, client: Client
) -> None:
    player = client.player if client.has_player else None
    if player is None:
        raise ImpossibleError(actually="is impossible")

    session = player.session

    feature_flags = FeatureFlags(features=["minecraft:vanilla"])
    tags = Tags(tags=[])

    session.locale = client_information.locale
    session.view_distance = client_information.view_distance
    session.chat_mode = client_information.chat_mode
    session.chat_colors = client_information.chat_colors
    session.displayed_skin_parts = client_information.displayed_skin_parts
    session.main_hand = client_information.main_hand
    session.enable_text_filtering = client_information.enable_text_filtering
    session.allow_server_listings = client_information.allow_server_listings
    session.particle_status = client_information.particle_status

    if session.locale == "en_gb":
        return await client.kick("вали назуй пиндос!!")

    await client.send_many(
        feature_flags,
        tags,
        Ping(
            id_=secrets.randbelow(2**31 - 1),
        ),
    )
    return None


@router.on(KeepAliveRequest)
async def on_login(keep_alive: KeepAliveRequest, client: Client) -> None:
    await client.send(
        KeepAliveResponse(keep_alive_id=keep_alive.keep_alive_id)
    )


@router.on(Pong)
async def on_pong(_pong: Pong, client: Client) -> None:
    await client.send(FinishConfigurationRequest())


@router.on(CustomPayload)
async def on_payload(
    payload: CustomPayload,
) -> None:
    pass


async def wait_and_teleport(client: Client) -> None:
    if client.session.chunk_ack_future:
        await asyncio.wait_for(client.session.chunk_ack_future, timeout=10.0)

    await client.send(
        Position(
            teleport_id=secrets.randbelow(2**31 - 1),
            x=0,
            y=-50,
            z=10,
            dx=0.0,
            dy=0.0,
            dz=0.0,
            yaw=0.0,
            pitch=0.0,
            flags=TeleportFlags.relative_pitch,
        ),
    )


@router.on(FinishConfigurationAcknowledge)
async def on_finish_configuration(
    _payload: FinishConfigurationAcknowledge,
    client: Client,
    properties: Properties,
    chunk_sender: ChunkSender,
    ticker: Ticker,
    world: World,
) -> None:
    player = client.player if client.has_player else None
    if player is None:
        raise ImpossibleError(actually="is impossible")

    session = player.session

    client.session.state = State.PLAY

    player_info = PlayerInfo(
        player_info=PlayerInfoUpdateStruct(
            actions_mask=0x01 | 0x04 | 0x08,
            players=[
                PlayerInfoActionStruct(
                    uuid=session.uuid,
                    name=session.username,
                    properties=[],
                    game_mode=0,
                    listed=True,
                    ping=0,
                )
            ],
        )
    )

    view_distance = properties.performance.view_distance
    player_entity_id = world.next_entity_id()
    chunks: set[tuple[int, int]] = set()

    for x in range(-view_distance, view_distance):
        for z in range(-view_distance, view_distance):
            chunks.add((x, z))

    await client.send_many(
        Login(
            entity_id=player_entity_id,
            is_hardcore=properties.world.hardcore,
            world_names=[
                "minecraft:overworld",
                "minecraft:the_nether",
                "minecraft:the_end",
            ],
            max_players=properties.server.max_players,
            view_distance=view_distance,
            simulation_distance=properties.performance.simulation_distance,
            reduced_debug_info=False,
            enable_respawn_screen=True,
            do_limited_crafting=False,
            world_state=WorldStateStruct(
                dimension_type=0,
                dimension_name="minecraft:overworld",
                hashed_seed=_seed_hash(seed=properties.world.seed),
                game_mode=1,
                previous_game_mode=0,
                is_debug=False,
                is_flat=True,
                has_death_location=False,
                death_dimension_name=None,
                death_location=None,
                portal_cooldown=3,
                sea_level=63,
            ),
            enforces_secure_chat=True,
        ),
        player_info,
        SetTickingState(tick_rate=ticker.TICK_RATE, is_frozen=False),
        Abilities(
            flags=AbilitiesFlags.CREATIVE, flying_speed=0.05, walking_speed=0.1
        ),
        HeldItemSlot(slot=0),
        Difficulty(difficulty=0, difficulty_locked=True),
        # TODO(IvanPythonov): add difficulty to properties
        EntityStatus(entity_id=player_entity_id, entity_status=0),
        GameStateChange(reason=13, game_mode=0.0),
        UpdateViewDistance(view_distance=view_distance),
        UpdateViewPosition(chunk_x=0, chunk_z=10 // 32),
        SpawnPosition(location=(0, 100, 10), angle=0.0),
    )

    await chunk_sender.load_chunks_batch(client=client, chunks=chunks)

    task = asyncio.create_task(
        wait_and_teleport(client=client),
        name=f"TeleportTask-{session.username or session.uuid}",
    )
    client.session.background_tasks.add(task)
    task.add_done_callback(client.session.background_tasks.discard)
