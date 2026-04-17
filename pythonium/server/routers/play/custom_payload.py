"""Custom Payload Router."""

from pythonium.engine.packets.ingoing.play import CustomPayload
from pythonium.server.routers.play import router as play_router


@play_router.on(CustomPayload)
async def custom_payload_handler(custom_payload: CustomPayload) -> None:
    pass
