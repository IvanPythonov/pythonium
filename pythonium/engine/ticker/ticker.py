import asyncio
import logging
import time

from pythonium.engine.world import World

logger = logging.getLogger(name=__name__)


class Ticker:
    """Ticker class."""

    TPS = 20
    TICK_TIME = 1.0 / TPS

    def __init__(self, world: World) -> None:
        self.current_tick = 0
        self.world = world

    async def run(self) -> None:
        next_tick = time.monotonic()

        while True:
            self.current_tick += 1

            start_logic = time.monotonic()

            duration = time.monotonic() - start_logic

            if duration > self.TICK_TIME and logger.isEnabledFor(
                logging.DEBUG
            ):
                logger.debug(
                    "Can't keep up! Tick took %s ms",
                    f"{duration * 1000:.2f}",
                )

            next_tick += self.TICK_TIME
            sleep_time = next_tick - time.monotonic()

            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
            elif sleep_time < -1.0:
                next_tick = time.monotonic()
