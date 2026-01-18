"""Some logic for router."""

import secrets
from logging import getLogger

from pythonium.engine import Client, Router
from pythonium.engine.enums import State
from pythonium.engine.packets import (
    AcknowledgeFinishConfiguration,
    ClientInformation,
    ConfigurationCustomPayload,
    Disconnect,
    FinishConfiguration,
    KeepAliveConfigurationRequest,
    KeepAliveConfigurationResponse,
    Login,
    Disconnect,
    PingConfiguration,
    PongConfiguration,
)

logger = getLogger(__name__)
router = Router(name=__name__)


@router.on(ClientInformation)
async def on_client_information(
    client_information: ClientInformation, client: Client
) -> PingConfiguration | Disconnect:
    return Disconnect(text="1111111111111")
    return PingConfiguration(
        id_=secrets.randbelow(2**31 - 1),
    )


@router.on(KeepAliveConfigurationRequest)
async def on_login(
    keep_alive: KeepAliveConfigurationRequest,
) -> KeepAliveConfigurationResponse:
    return KeepAliveConfigurationResponse(
        keep_alive_id=keep_alive.keep_alive_id
    )


@router.on(PongConfiguration)
async def on_pong(
    _pong: PongConfiguration,
) -> FinishConfiguration:
    return FinishConfiguration()


@router.on(ConfigurationCustomPayload)
async def on_payload(
    payload: ConfigurationCustomPayload,
) -> None: ...


@router.on(AcknowledgeFinishConfiguration)
async def on_finish_configuration(
    _payload: AcknowledgeFinishConfiguration, client: Client
) -> Login:
    client.session.state = State.PLAY

    return Login(
        entity_id=1,
        is_hardcore=False,
        dimension_names=["minecraft:overworld"],
        max_players=20,
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
        sea_level=63,
        enforces_secure_chat=False,
        death_dimension_name="minecraft:overworld",
        death_location=(0, 0, 0),
    )
