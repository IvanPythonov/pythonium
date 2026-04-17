"""Chunk Batch Received Router."""

from pythonium.engine.packets.ingoing.play import ChunkBatchReceived
from pythonium.server.routers.play import router as play_router


@play_router.on(ChunkBatchReceived)
async def chunk_batch_received_handler(
    chunk_batch: ChunkBatchReceived,
) -> None:
    pass
