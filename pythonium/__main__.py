"""Entrypoint."""

import asyncio
import atexit
import contextlib
import importlib
import logging
import queue
import sys
from logging.handlers import QueueHandler, QueueListener

from pythonium.engine import Server
from pythonium.engine.properties_reader import get_properties
from pythonium.server.routers import (
    configuration_router,
    handshake_router,
    login_router,
    status_router,
)
from pythonium.server.routers.play import router as play_router


def setup_async_logging(*, debug: bool) -> None:
    log_queue: queue.Queue = queue.Queue(-1)

    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    listener = QueueListener(
        log_queue, console_handler, respect_handler_level=True
    )

    queue_handler = QueueHandler(log_queue)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if debug else logging.INFO)
    root_logger.handlers.clear()
    root_logger.addHandler(queue_handler)

    listener.start()

    atexit.register(listener.stop)


async def main() -> None:
    properties = get_properties("properties.toml")

    setup_async_logging(debug=properties.server.debug)

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
        loop = importlib.import_module("uvloop")

        loop.install()
        return logger.info("Using %s", loop.__name__)

    return logger.info(
        "Using default asyncio loop. Recommended to install `uvloop` (Linux)"
    )


if __name__ == "__main__":
    _setup_asyncio_loop()

    asyncio.run(main=main())
