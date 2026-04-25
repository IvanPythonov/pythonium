"""Block Dig Event realization Router."""

from pythonium.engine.packets.ingoing import (
    BlockDig,
)
from pythonium.engine.packets.ingoing.play import BlockPlace
from pythonium.engine.router import Router
from pythonium.engine.world import World

router = Router(name=__name__)


@router.on(BlockDig)
async def on_block_dig(block_dig: BlockDig, world: World) -> None:
    if block_dig.status == 2:
        await world.remove_block(*block_dig.location)


@router.on(BlockPlace)
async def on_block_place(block_place: BlockPlace, world: World) -> None:
    x, y, z = block_place.location

    await world.set_block(x=x, y=y, z=z, block_id=1)
    await world.update_chunk()
