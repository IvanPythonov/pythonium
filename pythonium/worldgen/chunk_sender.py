import asyncio
from collections.abc import Iterable
from typing import TYPE_CHECKING

from pythonium.engine.packets.outgoing import (
    ChunkBatchFinished,
    ChunkBatchStart,
    MapChunk,
    MultiBlockChange,
    UnloadChunk,
)
from pythonium.engine.world import World

if TYPE_CHECKING:
    from pythonium.engine.client import Client


SECTION_SIZE = 16

SECTION_X_MASK = 0x3FFFFF
SECTION_Y_MASK = 0xFFFFF


def pack_section_position(
    section_x: int,
    section_y: int,
    section_z: int,
) -> int:
    packed = (
        ((section_x & SECTION_X_MASK) << 42)
        | (section_y & SECTION_Y_MASK)
        | ((section_z & SECTION_X_MASK) << 20)
    )
    if packed >= 1 << 63:
        packed -= 1 << 64
    return packed


def pack_block_change(
    block_state_id: int,
    local_x: int,
    local_y: int,
    local_z: int,
) -> int:
    return (block_state_id << 12) | (local_x << 8) | (local_z << 4) | local_y


def get_section_coords(
    block_x: int,
    block_y: int,
    block_z: int,
) -> tuple[int, int, int]:
    return (
        block_x >> 4,
        block_y >> 4,
        block_z >> 4,
    )


def get_local_coords(
    block_x: int,
    block_y: int,
    block_z: int,
) -> tuple[int, int, int]:
    return (
        block_x & 15,
        block_y & 15,
        block_z & 15,
    )


class ChunkSender:
    """Chunk sender."""

    def __init__(self, world: World) -> None:
        self.world = world

    async def load_chunk(
        self,
        client: Client,
        chunk_x: int,
        chunk_z: int,
    ) -> None:
        chunk = await self.world.get_chunk(
            x=chunk_x,
            z=chunk_z,
        )

        await client.send(
            MapChunk(
                x=chunk_x,
                z=chunk_z,
                heightmaps=chunk.get_heightmaps(),
                chunk_data=chunk.get_chunk_data(),
                block_entities=[],
                light_data=chunk.get_light_data(),
            )
        )

    async def load_chunks_batch(
        self,
        client: Client,
        chunks: Iterable[tuple[int, int]],
        batch_size: int = 32,
    ) -> None:
        chunks = list(chunks)
        total = len(chunks)

        if total == 0:
            return

        await client.send(ChunkBatchStart())

        sent = 0

        while sent < total:
            batch = chunks[sent : sent + batch_size]

            tasks = [self.load_chunk(client, x, z) for x, z in batch]

            await asyncio.gather(*tasks)

            sent += batch_size

        await client.send(ChunkBatchFinished(batch_size=total))

    async def unload_chunk(
        self,
        client: Client,
        chunk_x: int,
        chunk_z: int,
    ) -> None:
        await client.send(
            UnloadChunk(
                chunk_x=chunk_x,
                chunk_z=chunk_z,
            )
        )

    async def send_block_change(
        self,
        client: Client,
        block_x: int,
        block_y: int,
        block_z: int,
        block_state_id: int,
    ) -> None:
        section_x, section_y, section_z = get_section_coords(
            block_x,
            block_y,
            block_z,
        )

        local_x, local_y, local_z = get_local_coords(
            block_x,
            block_y,
            block_z,
        )

        section_position = pack_section_position(
            section_x,
            section_y,
            section_z,
        )

        record = pack_block_change(
            block_state_id=block_state_id,
            local_x=local_x,
            local_y=local_y,
            local_z=local_z,
        )

        await client.send(
            MultiBlockChange(
                chunk_coordinates=section_position,
                records=[record],
            )
        )
