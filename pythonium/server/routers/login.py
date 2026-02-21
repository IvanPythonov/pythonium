"""Logging Phase Router."""

from logging import getLogger

from pythonium.engine import Client, Router
from pythonium.engine.enums import State
from pythonium.engine.packets import (
    LoginAcknowledged,
    LoginCustomPayload,
    LoginStart,
    LoginSuccess,
)

logger = getLogger(__name__)
router = Router(name=__name__)


@router.on(LoginStart)
async def on_login(
    login_start: LoginStart,
) -> LoginSuccess:
    return LoginSuccess(
        uuid=login_start.uuid, name=login_start.name, is_legacy=False
    )


@router.on(LoginAcknowledged)
async def on_acknowledge(
    login_acknowledged: LoginAcknowledged,
    client: Client,
) -> None:
    logger.debug(login_acknowledged)

    client.session.state = State.CONFIGURATION


@router.on(LoginCustomPayload)
async def on_payload(
    payload: LoginCustomPayload,
) -> None:
    logger.debug(payload)
