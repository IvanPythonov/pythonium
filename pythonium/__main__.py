"""Entrypoint."""

import asyncio
import logging

from pythonium.engine import Server
from pythonium.server.routers import handshake_router

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    server = Server()

    server.include_router(handshake_router)

    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
