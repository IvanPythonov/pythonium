"""Block Dig Event realization Router."""

from pythonium.engine.packets.ingoing import (
    BlockDig,
)
from pythonium.engine.router import Router
from pythonium.engine.world import World

router = Router(name=__name__)


@router.on(BlockDig)
async def on_block_dig(block_dig: BlockDig, world: World) -> None:
    if block_dig.status == 2:
        await world.remove_block(*block_dig.location)
    
    
