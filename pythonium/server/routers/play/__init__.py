"""Play Phase Router Init."""

import importlib
import pkgutil
from pathlib import Path

from .base import router

current_dir = Path(__file__).resolve().parent

for _, module_name, __ in pkgutil.iter_modules([str(current_dir)]):
    if module_name in ("base", "__init__"):
        continue

    full_module_name = f"{__name__}.{module_name}"

    importlib.import_module(full_module_name)

__all__ = ("router",)
