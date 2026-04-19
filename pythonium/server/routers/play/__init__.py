"""Play Phase Router Init."""

import importlib
import pkgutil
from pathlib import Path

from .base import router as play_router


def play_router_bake() -> None:
    current_dir = Path(__file__).resolve().parent

    for _, module_name, __ in pkgutil.iter_modules([str(current_dir)]):
        if module_name in ("base", "__init__"):
            continue

        full_module_name = f"{__name__}.{module_name}"

        router = importlib.import_module(full_module_name).router

        play_router.include_router(router)


play_router_bake()
__all__ = ("play_router",)
