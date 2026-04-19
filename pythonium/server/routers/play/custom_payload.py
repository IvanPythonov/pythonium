"""Custom Payload Router."""

from pythonium.engine.packets.ingoing.play import CustomPayload
from pythonium.engine.router import Router

router = Router(name=__name__)


@router.on(CustomPayload)
async def custom_payload_handler(custom_payload: CustomPayload) -> None:
    pass
