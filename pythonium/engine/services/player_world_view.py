import asyncio
from dataclasses import dataclass

from pythonium.engine import Client
from pythonium.engine.exceptions import ImpossibleError
from pythonium.engine.packets.outgoing import UpdateViewPosition
from pythonium.worldgen.chunk_sender import ChunkSender


@dataclass
class ChunkDiff:
    """Chunk difference."""

    to_load: set[tuple[int, int]]
    to_unload: set[tuple[int, int]]


class WorldViewService:
    """World View Service."""

    def __init__(self, chunk_sender: ChunkSender, view_distance: int) -> None:
        self.chunk_sender = chunk_sender
        self.view_distance = view_distance

    async def update_position(self, client: Client, x: int, z: int) -> None:
        player = client.player if client.has_player else None

        if player is None:
            raise ImpossibleError(actually="this is impossible")

        session = player.session

        new_center = (x >> 4, z >> 4)

        if session.last_chunk_center == new_center:
            return

        old_center = session.last_chunk_center or new_center

        session.last_chunk_center = new_center

        view_distance = self.view_distance or 8

        new_set = self._chunks_around(new_center, view_distance)
        old_set = self._chunks_around(old_center, view_distance)

        diff = ChunkDiff(
            to_load=new_set - old_set,
            to_unload=old_set - new_set,
        )

        await self._apply(client, diff)

        session.loaded_chunks = new_set

        await client.send(
            UpdateViewPosition(
                chunk_x=new_center[0],
                chunk_z=new_center[1],
            )
        )

    async def _apply(self, client: Client, diff: ChunkDiff) -> None:
        if diff.to_unload:
            await asyncio.gather(
                *(
                    self.chunk_sender.unload_chunk(client, x, z)
                    for x, z in diff.to_unload
                )
            )

        if diff.to_load:
            await self.chunk_sender.load_chunks_batch(
                client=client,
                chunks=diff.to_load,
            )

    def _chunks_around(
        self, center: tuple[int, int], view_distance: int
    ) -> set[tuple[int, int]]:
        cx, cz = center

        return {
            (x, z)
            for x in range(cx - view_distance, cx + view_distance + 1)
            for z in range(cz - view_distance, cz + view_distance + 1)
        }
