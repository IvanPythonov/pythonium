import asyncio
import logging
import time
from collections import deque

from pythonium.engine.world import World

logger = logging.getLogger(name=__name__)


class TickMetrics:
    """Tick Metrics class."""

    tps: float
    tick_time_ms: float


class Ticker:
    """Ticker class."""

    TICK_RATE = 20.0

    TPS = 20
    TICK_TIME = 1.0 / TPS

    def __init__(self, world: World) -> None:
        self.current_tick = 0
        self.tick_metrics = TickMetrics()

        self.world = world

        self._samples: deque[float] = deque(maxlen=100)
        self._last_tick_time: float = time.monotonic()

    async def run(self) -> None:
        next_tick = time.monotonic()

        while True:
            self.current_tick += 1

            start_logic = time.monotonic()

            self.world.tick(current_tick=self.current_tick)

            logic_time = time.monotonic() - start_logic

            now = time.monotonic()

            dt = now - self._last_tick_time
            self._last_tick_time = now

            self._samples.append(dt)

            avg = sum(self._samples) / len(self._samples)
            tps = min(1.0 / avg, self.TPS)

            self.tick_metrics.tps = tps
            self.tick_metrics.tick_time_ms = logic_time * 1000

            if logic_time > self.TICK_TIME and logger.isEnabledFor(
                logging.DEBUG
            ):
                logger.debug(
                    "Can't keep up! Tick took %s ms",
                    f"{logic_time * 1000:.2f}",
                )

            next_tick += self.TICK_TIME
            sleep_time = next_tick - time.monotonic()

            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
            elif sleep_time < -1.0:
                next_tick = time.monotonic()
