"""Block interaction router."""

from nbtlib import String

from pythonium.engine import Client
from pythonium.engine.entity.item_entity import ItemEntity
from pythonium.engine.entity.tracker import EntityTracker
from pythonium.engine.enums.player_action import PlayerActionStatus
from pythonium.engine.packets.ingoing import BlockDig
from pythonium.engine.packets.ingoing.play import BlockPlace
from pythonium.engine.router import Router
from pythonium.engine.server.client_manager import ClientManager
from pythonium.engine.world import World
from pythonium.registries.block_registry import BLOCK_REGISTRY
from pythonium.worldgen.chunk_sender import ChunkSender

router = Router(name=__name__)


@router.on(BlockDig)
async def on_block_dig(
    packet: BlockDig,
    world: World,
    client_manager: ClientManager,
    entity_tracker: EntityTracker,
    chunk_sender: ChunkSender,
) -> None:
    if packet.status not in (
        PlayerActionStatus.FINISH_DIGGING,
        PlayerActionStatus.START_DIGGING,
    ):
        return

    block_x, block_y, block_z = packet.location

    chunk = await world.get_chunk(block_x >> 4, block_z >> 4)
    state_id = chunk.get_block(block_x, block_y, block_z)
    item_id = BLOCK_REGISTRY.get_drop_for_state(state_id)

    await world.remove_block(
        block_x,
        block_y,
        block_z,
    )

    for client in client_manager:
        await chunk_sender.send_block_change(
            client=client,
            block_x=block_x,
            block_y=block_y,
            block_z=block_z,
            block_state_id=0,  # Воздух (блок сломан)
        )

    item = ItemEntity(
        x=block_x + 0.5, y=block_y, z=block_z + 0.5, item_id=item_id
    )
    await world.spawn_entity(item)
    await entity_tracker.spawn_entity(item)


@router.on(BlockPlace)
async def on_block_place(
    packet: BlockPlace,
    world: World,
    client_manager: ClientManager,
    chunk_sender: ChunkSender,
) -> None:
    block_x, block_y, block_z = packet.location

    offset_x, offset_y, offset_z = packet.direction_.offset

    target_x = block_x + offset_x
    target_y = block_y + offset_y
    target_z = block_z + offset_z

    block_state_id = 1

    await world.set_block(
        x=target_x,
        y=target_y,
        z=target_z,
        block_id=block_state_id,
    )

    for client in client_manager:
        await chunk_sender.send_block_change(
            client=client,
            block_x=target_x,
            block_y=target_y,
            block_z=target_z,
            block_state_id=block_state_id,
        )
