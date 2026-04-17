"""Animation Event realization Router."""

from pythonium.engine.packets.ingoing import (
    ArmAnimation,
)
from pythonium.server.routers.play import router as play_router


@play_router.on(ArmAnimation)
async def on_arm_animation(
    arm_animation: ArmAnimation,
) -> None:
    pass
