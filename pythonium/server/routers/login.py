"""Logging Phase Router."""

import hashlib
from logging import getLogger
from uuid import UUID

from pythonium.engine import Client, Router
from pythonium.engine.enums import State
from pythonium.engine.packets import (
    LoginAcknowledged,
    LoginCustomPayload,
    LoginStart,
    LoginSuccess,
)
from pythonium.engine.properties_reader import Properties

logger = getLogger(__name__)
router = Router(name=__name__)


@router.on(LoginStart)
async def on_login(
    login_start: LoginStart, client: Client, properties: Properties
) -> None:
    player_uuid = login_start.uuid

    if not properties.auth.online_mode:
        player_uuid = str(
            UUID(
                bytes=hashlib.md5(  # noqa: S324
                    f"OfflinePlayer:{login_start.name}".encode()
                ).digest()[:16],
                version=3,
            )
        )

    await client.send(
        LoginSuccess(uuid=player_uuid, name=login_start.name, is_legacy=False)
    )


@router.on(LoginAcknowledged)
async def on_acknowledge(
    _login_acknowledged: LoginAcknowledged,
    client: Client,
) -> None:
    client.session.state = State.CONFIGURATION


@router.on(LoginCustomPayload)
async def on_payload(
    _payload: LoginCustomPayload,
) -> None:
    pass
