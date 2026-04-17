"""Block Dig Event realization Router."""

from pythonium.engine.packets.ingoing import (
    BlockDig,
)
from pythonium.server.routers.play import router as play_router


@play_router.on(BlockDig)
async def on_block_dig(
    block_dig: BlockDig,
) -> None:
    pass
