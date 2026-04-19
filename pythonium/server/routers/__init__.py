from .configuration import router as configuration_router
from .handshake import router as handshake_router
from .login import router as login_router
from .play import play_router
from .status import router as status_router

__all__ = (
    "configuration_router",
    "handshake_router",
    "login_router",
    "play_router",
    "status_router",
)
