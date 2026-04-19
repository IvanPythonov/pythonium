"""Move Player Rot realization Router."""

import asyncio

from nbtlib.tag import Compound, List, String

from pythonium.engine.client.client import Client
from pythonium.engine.packets.ingoing import (
    PositionLook,
)
from pythonium.engine.packets.ingoing.play import Flying, Look, Position
from pythonium.engine.packets.outgoing.play import (
    ChunkBatchFinished,
    ChunkBatchStart,
    MapChunk,
    SystemChat,
    UnloadChunk,
    UpdateViewPosition,
)
from pythonium.engine.properties_reader import Properties
from pythonium.engine.router import Router
from pythonium.engine.ticker.ticker import Ticker
from pythonium.engine.world import World

router = Router(name=__name__)


@router.on(Position, PositionLook)
async def on_move_player_rot(
    move_player_rot: Position | PositionLook,
    properties: Properties,
    client: Client,
    world: World,
    ticker: Ticker,
) -> None:
    x = move_player_rot.x
    z = move_player_rot.z

    view_distance = int(properties.performance.view_distance)

    player_cx = int(x // 16)
    player_cz = int(z // 16)

    new_center = (player_cx, player_cz)

    current_chunks = client.session.visible_chunks

    target_chunks = {
        (cx, cz)
        for cx in range(
            player_cx - view_distance, player_cx + view_distance + 1
        )
        for cz in range(
            player_cz - view_distance, player_cz + view_distance + 1
        )
    }

    to_load = target_chunks - current_chunks
    to_unload = current_chunks - target_chunks

    if not to_load and not to_unload:
        return

    client.session.last_chunk_center = new_center

    await client.send(
        SystemChat(
            content={
                "text": String(""),
                "extra": List[Compound](
                    [
                        {
                            "text": String(
                                f"[Chunks] center={new_center}"
                                f"; load={len(to_load)}; "
                                f"unload={len(to_unload)}"
                            ),
                            "color": String("gray"),
                        },
                        {"text": String("\n")},
                        {
                            "text": String(
                                f"[Ticker] TPS={ticker.tick_metrics.tps}; "
                                f"tick={ticker.tick_metrics.tick_time_ms:} ms"
                            ),
                            "color": String("green"),
                        },
                    ]
                ),
            },
            is_action_bar=False,
        )
    )

    sorted_to_load = sorted(
        to_load,
        key=lambda c: (c[0] - player_cx) ** 2 + (c[1] - player_cz) ** 2,
    )

    chunks_data = await asyncio.gather(
        *(world.get_chunk(cx, cz) for cx, cz in sorted_to_load)
    )

    loaded_packets: list[MapChunk] = []

    for (cx, cz), world_chunk in zip(
        sorted_to_load, chunks_data, strict=False
    ):
        if world_chunk is None:
            continue

        loaded_packets.append(
            MapChunk(
                x=cx,
                z=cz,
                heightmaps=world_chunk.get_heightmaps(),
                chunk_data=world_chunk.get_chunk_data(),
                block_entities=[],
                light_data=world_chunk.get_light_data(),
            )
        )

    unload_packets = [
        UnloadChunk(chunk_x=cx, chunk_z=cz) for cx, cz in to_unload
    ]

    if not client.session.chunk_send_lock:
        msg = "Chunk send lock is not initialized"
        raise RuntimeError(msg)

    async with client.session.chunk_send_lock:
        await client.send(
            UpdateViewPosition(chunk_x=player_cx, chunk_z=player_cz)
        )
        await client.send_many(
            ChunkBatchStart(),
            *unload_packets,
            *loaded_packets,
            ChunkBatchFinished(batch_size=len(loaded_packets)),
        )

    client.session.visible_chunks = target_chunks


@router.on(Flying)
async def on_flying(flying: Flying) -> None: ...


@router.on(Look)
async def on_look(look: Look) -> None: ...
