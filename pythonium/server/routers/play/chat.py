"""Chat Command Router."""

import secrets

from nbtlib.tag import String

from pythonium.engine.client.client import Client
from pythonium.engine.enums.teleport_flags import TeleportFlags
from pythonium.engine.packets.ingoing.play import ChatCommand, ChatMessage
from pythonium.engine.packets.outgoing.play import (
    Abilities,
    Position,
    SystemChat,
)
from pythonium.engine.router import Router

router = Router(name=__name__)


@router.on(ChatCommand)
async def chat_command_handler(
    chat_command: ChatCommand, client: Client
) -> None:
    args = chat_command.command.split()
    command = args[0]

    if command == "fly":
        fly_speed = args[1] if len(args) > 1 else "0.05"

        await client.send(
            Abilities(
                flags=0x04, flying_speed=float(fly_speed), walking_speed=0.1
            )
        )
    elif command == "walk":
        walk_speed = args[1] if len(args) > 1 else "0.1"

        await client.send(
            Abilities(
                flags=0x00, flying_speed=0.0, walking_speed=float(walk_speed)
            )
        )
    elif command == "tp":
        if len(args) < 3:
            return

        x = float(args[1])
        y = float(args[2])
        z = float(args[3])

        await client.send(
            Position(
                x=x,
                y=y,
                z=z,
                dx=0.0,
                dy=0.0,
                dz=0.0,
                yaw=0.0,
                pitch=0.0,
                teleport_id=secrets.randbelow(2**31),
                flags=TeleportFlags.absolute,
            )
        )


@router.on(ChatMessage)
async def on_chat_message(chat_message: ChatMessage, client: Client) -> None:
    await client.send(
        SystemChat(
            content={
                "text": String(
                    f"<{client.session.username}>: {chat_message.message}"
                )
            },
            is_action_bar=False,
        )
    )
