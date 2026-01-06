import inspect
from collections.abc import Callable
from typing import Any, Self

from pythonium.engine.packets import Packet

type Handler = Callable[..., Any]


class Router:
    """Router can route updates."""

    def __init__(self, *, name: str | None = None, **kwargs: object) -> None:
        self.name = name or hex(id(self))

        self._parent_router: Router | None = None
        self.sub_routers: list[Router] = []
        self._commands: dict[str, Handler] = {}

        self._kwargs = kwargs

    def on(self, *commands_type: type[Packet]) -> Callable[[Handler], Handler]:
        def decorator(
            func: Handler,
        ) -> Handler:
            for command_type in commands_type:
                self._commands[command_type.__name__] = func
            return func

        return decorator

    def startup(self) -> Callable[[Handler], Handler]:
        def decorator(
            func: Handler,
        ) -> Handler:
            self._commands["startup"] = func
            return func

        return decorator

    @property
    def commands(self) -> dict[str, Handler]:
        return self._commands

    @property
    def all_commands(self) -> dict[str, Handler]:
        """Get all commands from this router and sub-routers."""
        commands = self._commands.copy()
        for sub_router in self.sub_routers:
            commands.update(sub_router.all_commands)
        return commands

    @property
    def parent_router(self) -> Router | None:  # pyright: ignore[reportUndefinedVariable]
        return self._parent_router

    @parent_router.setter
    def parent_router(self, router: Self) -> None:
        """Set the parent router for this router."""
        if not isinstance(router, Router):
            msg = (
                "router should be instance of "
                f"Router not {type(router).__name__!r}"
            )
            raise TypeError(msg)
        if self._parent_router:
            msg = f"Router is already attached to {self._parent_router!r}"
            raise RuntimeError(msg)
        if self == router:
            msg = "Self-referencing routers is not allowed"
            raise RuntimeError(msg)

        parent: Router | None = router
        while parent is not None:
            if parent == self:
                msg = "Circular referencing of Router is not allowed"
                raise RuntimeError(msg)

            parent = parent.parent_router

        self._parent_router = router
        router.sub_routers.append(self)

    def include_routers(self, *routers: Self) -> None:
        """Attach multiple routers."""
        if not routers:
            msg = "At least one router must be provided"
            raise ValueError(msg)
        for router in routers:
            self.include_router(router)

    def include_router(self, router: Router) -> Router:  # pyright: ignore[reportUndefinedVariable]
        """Attach another router."""
        if not isinstance(router, Router):
            msg = (
                "router should be instance of "
                f"Router not {type(router).__class__.__name__}"
            )
            raise TypeError(msg)
        router.parent_router = self
        self._commands.update(router.commands)
        return self

    async def route(self, packet: Packet) -> object:
        """Route command to appropriate handler."""
        func = self.resolve_router(packet=type(packet))

        if func is None:
            return None

        sig_params = set(inspect.signature(func).parameters.keys())
        kwargs = {k: v for k, v in self._kwargs.items() if k in sig_params}

        return await func(packet, **kwargs)

    def resolve_router(self, packet: type[Packet]) -> Handler | None:
        packet_name = packet.__name__

        if packet_name in self._commands:
            return self._commands[packet_name]
        return None

    def __str__(self) -> str:
        """Return string representation of the router."""
        return f"{type(self).__name__} {self.name!r}"
