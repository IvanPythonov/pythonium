"""Entrypoint."""

import asyncio
import contextlib
import importlib
import logging
import sys

from pythonium.engine import Server
from pythonium.server.routers import (
    configuration_router,
    handshake_router,
    login_router,
    status_router,
)
from pythonium.server.routers.play import router as play_router

logging.basicConfig(level=logging.DEBUG)


async def main() -> None:
    server = Server()

    server.router.include_routers(
        handshake_router,
        status_router,
        login_router,
        configuration_router,
        play_router,
    )

    await server.serve()


def _setup_asyncio_loop() -> None:
    logger = logging.getLogger(name=__name__)

    with contextlib.suppress(ImportError):
        if sys.platform in ("win32", "cygwin"):
            loop = importlib.import_module("winloop")
        else:
            loop = importlib.import_module("uvloop")

        loop.install()
        return logger.info("Using %s", loop.__name__)

    return logger.info(
        "Using default asyncio loop. Recommended to "
        "install `uvloop` (Linux) or"
        "`winloop` (Windows)"
    )


if __name__ == "__main__":
    _setup_asyncio_loop()

    asyncio.run(main=main())
