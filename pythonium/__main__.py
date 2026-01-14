"""Entrypoint."""

import asyncio
import logging

from pythonium.engine import Server
from pythonium.server.routers import (
    configuration_router,
    handshake_router,
    login_router,
    status_router,
)

logging.basicConfig(level=logging.DEBUG)


async def main() -> None:
    server = Server()

    server.include_routers(
        handshake_router, status_router, login_router, configuration_router
    )

    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
