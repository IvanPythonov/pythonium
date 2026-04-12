"""Configuration Phase Router."""

import hashlib
import secrets
from logging import getLogger

from pythonium.engine import Client, Router
from pythonium.engine.codecs.chunk import LightDataStruct
from pythonium.engine.codecs.tag import RegistryTagsStruct, TagStruct
from pythonium.engine.codecs.world import WorldStateStruct
from pythonium.engine.enums import State
from pythonium.engine.enums.teleport_flags import TeleportFlags
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
    HeldItemSlot,
    Login,
    MapChunk,
    Position,
    SpawnPosition,
    UpdateViewPosition,
)
from pythonium.engine.properties_reader import Properties
from pythonium.registries.registries_storage import REGISTRY_PACKETS

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


@router.on(Settings)
async def on_client_information(
    client_information: Settings, client: Client
) -> None:
    feature_flags = FeatureFlags(features=["minecraft:vanilla"])
    tags = Tags(tags=[])

    client.session.locale = client_information.locale
    client.session.view_distance = client_information.view_distance
    client.session.chat_mode = client_information.chat_mode
    client.session.chat_colors = client_information.chat_colors
    client.session.displayed_skin_parts = (
        client_information.displayed_skin_parts
    )
    client.session.main_hand = client_information.main_hand
    client.session.enable_text_filtering = (
        client_information.enable_text_filtering
    )
    client.session.allow_server_listings = (
        client_information.allow_server_listings
    )
    client.session.particle_status = client_information.particle_status

    if client.session.locale == "en_gb":
        return await client.kick("вали назуй пиндос!!")

    await client.send_many(
        feature_flags,
        *REGISTRY_PACKETS,
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


@router.on(FinishConfigurationAcknowledge)
async def on_finish_configuration(
    _payload: FinishConfigurationAcknowledge,
    client: Client,
    properties: Properties,
) -> None:
    client.session.state = State.PLAY

    await client.send_many(
        Login(
            entity_id=1,
            is_hardcore=properties.world.hardcore,
            world_names=["minecraft:overworld"],
            max_players=properties.server.max_players,
            view_distance=properties.performance.view_distance,
            simulation_distance=properties.performance.simulation_distance,
            reduced_debug_info=False,
            enable_respawn_screen=True,
            do_limited_crafting=False,
            world_state=WorldStateStruct(
                dimension_type=0,
                dimension_name="minecraft:overworld",
                hashed_seed=1,
                # hashed_seed=_seed_hash(seed=properties.world.seed),
                game_mode=0,
                previous_game_mode=0,
                is_debug=False,
                is_flat=False,
                has_death_location=False,
                death_dimension_name=None,
                death_location=None,
                portal_cooldown=3,
                sea_level=63,
            ),
            enforces_secure_chat=True,
        ),
        SpawnPosition(
            location=(0, 10, 0),
            angle=0.0,
        ),
        Abilities(flags=0x00, flying_speed=0.05, walking_speed=0.1),
        HeldItemSlot(slot=0),
        Difficulty(difficulty=0, difficulty_locked=True),
        # TODO(IvanPythonov): add difficulty to properties
        EntityStatus(entity_id=1, entity_status=0),
        UpdateViewPosition(chunk_x=0, chunk_z=0),
        Position(
            teleport_id=0,
            x=0,
            y=10,
            z=10,
            dx=0.0,
            dy=0.0,
            dz=0.0,
            yaw=0.0,
            pitch=0.0,
            flags=TeleportFlags.relative_pitch,
        ),
        MapChunk(
            x=0,
            z=0,
            heightmaps={},
            chunk_data=b"\0x",
            block_entities=[],
            light_data=LightDataStruct(
                sky_y_mask=[],
                block_y_mask=[],
                empty_block_y_mask=[],
                empty_sky_y_mask=[],
                sky_updates=[],
                block_updates=[],
            ),
        ),
    )
