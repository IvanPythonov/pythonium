"""Slot realization router."""

from pythonium.engine.packets.ingoing import SetCreativeSlot, HeldItemSlot
from pythonium.engine.router import Router

router = Router(name=__name__)


@router.on(SetCreativeSlot)
async def on_set_creative_slot(
    set_creative_slot: SetCreativeSlot,
) -> None:
    print(set_creative_slot)


@router.on(HeldItemSlot)
async def on_held_item_slot(
    held_item_slot: HeldItemSlot,
) -> None:
    print(held_item_slot)
