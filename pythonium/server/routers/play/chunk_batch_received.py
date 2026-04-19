"""Chunk Batch Received Router."""

from pythonium.engine.client.client import Client
from pythonium.engine.packets.ingoing.play import ChunkBatchReceived
from pythonium.engine.router import Router

router = Router(name=__name__)


@router.on(ChunkBatchReceived)
async def chunk_batch_received_handler(
    _chunk_batch: ChunkBatchReceived, client: Client
) -> None:
    chunk_ack_future = client.session.chunk_ack_future

    if chunk_ack_future and not chunk_ack_future.done():
        chunk_ack_future.set_result(True)
