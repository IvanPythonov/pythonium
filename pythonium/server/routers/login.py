"""Logging Phase Router."""

import hashlib
from logging import getLogger
from uuid import UUID

from pythonium.engine import Client, Router
from pythonium.engine.enums import State
from pythonium.engine.packets.ingoing import (
    LoginAcknowledged,
    LoginStart,
)
from pythonium.engine.packets.outgoing.login import LoginPluginRequest, Success
from pythonium.engine.properties_reader import Properties

logger = getLogger(__name__)
router = Router(name=__name__)


@router.on(LoginStart)
async def on_login(
    login_start: LoginStart, client: Client, properties: Properties
) -> None:
    player_uuid = login_start.player_uuid

    if not properties.auth.online_mode:
        player_uuid = str(
            UUID(
                bytes=hashlib.md5(
                    f"OfflinePlayer:{login_start.username}".encode(),
                    usedforsecurity=False,
                ).digest()[:16],
                version=3,
            )
        )

    client.session.uuid = player_uuid
    client.session.username = login_start.username

    await client.send(
        Success(uuid=player_uuid, name=login_start.username, is_legacy=False)
    )


@router.on(LoginAcknowledged)
async def on_acknowledge(
    _login_acknowledged: LoginAcknowledged,
    client: Client,
) -> None:
    client.session.state = State.CONFIGURATION


@router.on(LoginPluginRequest)
async def on_payload(
    _payload: LoginPluginRequest,
) -> None:
    pass
