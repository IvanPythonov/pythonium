"""Configuration Phase Router."""

import secrets
from logging import getLogger

from pythonium.engine import Client, Router
from pythonium.engine.enums import State
from pythonium.engine.enums.teleport_flags import TeleportFlags
from pythonium.engine.packets import (
    AcknowledgeFinishConfiguration,
    ClientInformation,
    ConfigurationCustomPayload,
    FinishConfiguration,
    KeepAliveConfigurationRequest,
    KeepAliveConfigurationResponse,
    Login,
    PingConfiguration,
    PongConfiguration,
    SetDefaultSpawnPosition,
    SynchronizePlayerPosition,
)
from pythonium.registries.registries_storage import REGISTRY_PACKETS

logger = getLogger(__name__)
router = Router(name=__name__)


@router.on(ClientInformation)
async def on_client_information(
    client_information: ClientInformation, client: Client
) -> None:
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
        *REGISTRY_PACKETS,
        PingConfiguration(
            id_=secrets.randbelow(2**31 - 1),
        ),
    )
    return None


@router.on(KeepAliveConfigurationRequest)
async def on_login(
    keep_alive: KeepAliveConfigurationRequest, client: Client
) -> None:
    await client.send(
        KeepAliveConfigurationResponse(keep_alive_id=keep_alive.keep_alive_id)
    )


@router.on(PongConfiguration)
async def on_pong(_pong: PongConfiguration, client: Client) -> None:
    await client.send(FinishConfiguration())


@router.on(ConfigurationCustomPayload)
async def on_payload(
    payload: ConfigurationCustomPayload,
) -> None:
    pass


@router.on(AcknowledgeFinishConfiguration)
async def on_finish_configuration(
    _payload: AcknowledgeFinishConfiguration, client: Client
) -> None:
    client.session.state = State.PLAY

    await client.send_many(
        Login(
            entity_id=1,
            is_hardcore=False,
            dimension_names=["minecraft:overworld"],
            max_players=100,
            view_distance=10,
            simulation_distance=10,
            reduced_debug_info=False,
            enable_respawn_screen=True,
            do_limited_crafting=False,
            dimension_type=0,
            dimension_name="minecraft:overworld",
            hashed_seed=0,
            game_mode=0,
            previous_game_mode=-1,
            is_debug=False,
            is_flat=False,
            has_death_location=False,
            portal_cooldown=0,
        ),
        SetDefaultSpawnPosition(
            spawn_position=(0, 10, 0),
            angle=0.0,
        ),
        SynchronizePlayerPosition(
            teleport_id=0,
            x=0,
            y=10,
            z=10,
            velocity_x=0.0,
            velocity_y=0.0,
            velocity_z=0.0,
            yaw=0.0,
            pitch=0.0,
            flags=TeleportFlags.relative_pitch,
        ),
    )
