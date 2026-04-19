"""Animation Event realization Router."""

from pythonium.engine.packets.ingoing import (
    ArmAnimation,
)
from pythonium.engine.router import Router

router = Router(name=__name__)


@router.on(ArmAnimation)
async def on_arm_animation(
    arm_animation: ArmAnimation,
) -> None:
    pass
