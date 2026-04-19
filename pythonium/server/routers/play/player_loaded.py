"""Player Loaded Event realization Router."""

from pythonium.engine.client.client import Client
from pythonium.engine.codecs.node import NodeStruct
from pythonium.engine.packets.ingoing import (
    PlayerLoaded,
)
from pythonium.engine.packets.outgoing.play import DeclareCommands
from pythonium.engine.router import Router

router = Router(name=__name__)


@router.on(PlayerLoaded)
async def send_command_graph_on_join(
    _player_loaded: PlayerLoaded, client: Client
) -> None:

    command_nodes = [
        NodeStruct(
            flags=0x00,
            children=[1, 2],
        ),
        NodeStruct(
            flags=0x05,
            children=[],
            name="ping",
        ),
        NodeStruct(
            flags=0x01,
            children=[3],
            name="tp",
        ),
        NodeStruct(
            flags=0x02,
            children=[4],
            name="x",
            parser_id=2,
            properties=b"\x00",
        ),
        NodeStruct(
            flags=0x02,
            children=[5],
            name="y",
            parser_id=2,
            properties=b"\x00",
        ),
        NodeStruct(
            flags=0x06,
            children=[],
            name="z",
            parser_id=2,
            properties=b"\x00",
        ),
    ]

    await client.send(
        DeclareCommands(
            nodes=command_nodes,
            root_index=0,
        )
    )
