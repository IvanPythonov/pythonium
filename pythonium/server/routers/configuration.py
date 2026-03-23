"""Configuration Phase Router."""

import secrets
from logging import getLogger

from pythonium.engine import Client, Router
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
    FinishConfiguration as FinishConfigurationAcknowledge,
)
from pythonium.engine.packets.outgoing.configuration import (
    KeepAlive as KeepAliveResponse,
)
from pythonium.engine.packets.outgoing.configuration import (
    Ping,
)
from pythonium.engine.packets.outgoing.play import (
    Login,
    Position,
    SpawnPosition,
)
from pythonium.engine.properties_reader import Properties
from pythonium.registries.registries_storage import REGISTRY_PACKETS

logger = getLogger(__name__)
router = Router(name=__name__)


@router.on(Settings)
async def on_client_information(
    client_information: Settings, client: Client
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
                hashed_seed=0,
                game_mode=0,
                previous_game_mode=0,
                is_debug=False,
                is_flat=False,
                has_death_location=False,
                death_dimension_name=None,
                death_location=None,
                portal_cooldown=3,
                sea_level=1,
            ),
            enforces_secure_chat=True,
        ),
        SpawnPosition(
            location=(0, 10, 0),
            angle=0.0,
        ),
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
    )
