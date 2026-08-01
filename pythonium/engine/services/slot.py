from pythonium.engine import Client


class InventoryService:
    """Inventory Service."""

    def __init__(
        self,
        client: Client,
    ) -> None:
        self.client = client
        self.state = client.session

    async def use_slot(self, slot_id: int) -> None:
        new_center = (x >> 4, z >> 4)

        if self.state.last_chunk_center == new_center:
            return

        old_center = self.state.last_chunk_center or new_center

        self.state.last_chunk_center = new_center

        view_distance = self.view_distance or 8

        new_set = self._chunks_around(new_center, view_distance)
        old_set = self._chunks_around(old_center, view_distance)

        diff = ChunkDiff(
            to_load=new_set - old_set,
            to_unload=old_set - new_set,
        )

        await self._apply(diff)

        self.state.loaded_chunks = new_set

        await self.client.send(
            UpdateViewPosition(
                chunk_x=new_center[0],
                chunk_z=new_center[1],
            )
        )
