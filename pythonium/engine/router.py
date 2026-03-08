import inspect
from collections.abc import Awaitable, Callable
from functools import cache
from typing import Any, Self

from pythonium.engine.packets import Packet

type Handler = Callable[..., Awaitable[None]]


@cache
def _get_func_params(func: Handler) -> frozenset[str]:
    return frozenset(inspect.signature(func).parameters.keys())


def _resolve_kwargs(
    current_kwargs: dict[str, Any], func: Handler
) -> dict[str, Any]:
    sig_params = _get_func_params(func)

    return {k: current_kwargs[k] for k in sig_params if k in current_kwargs}


class Router:
    """Router can route updates."""

    def __init__(
        self, *, name: str | None = None, **kwargs: dict[str, Any]
    ) -> None:
        self.name = name or hex(id(self))

        self._parent_router: Router | None = None
        self.sub_routers: list[Router] = []
        self._commands: dict[tuple[int, int], Handler] = {}

        self._kwargs = kwargs

    def on(self, *commands_type: type[Packet]) -> Callable[[Handler], Handler]:
        def decorator(
            func: Handler,
        ) -> Handler:
            for command_type in commands_type:
                self._commands[
                    (command_type.__state__, command_type.packet_id)
                ] = func
            return func

        return decorator

    @property
    def commands(self) -> dict[tuple[int, int], Handler]:
        return self._commands

    @property
    def all_commands(self) -> dict[tuple[int, int], Handler]:
        """Get all commands from this router and sub-routers."""
        commands = self._commands.copy()
        for sub_router in self.sub_routers:
            commands.update(sub_router.all_commands)
        return commands

    @property
    def parent_router(self) -> "Router | None":  # pyright: ignore[reportUndefinedVariable]
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

    def include_routers(self, *routers: "Router") -> None:
        """Attach multiple routers."""
        if not routers:
            msg = "At least one router must be provided"
            raise ValueError(msg)
        for router in routers:
            self.include_router(router)

    def include_router(self, router: "Router") -> "Router":  # pyright: ignore[reportUndefinedVariable]
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

    async def route(self, packet: Packet, **kwargs: object) -> None:
        """Route command to appropriate handler."""
        func = self.resolve_router(packet=type(packet))

        if func is None:
            return None

        kwargs = _resolve_kwargs(
            current_kwargs=kwargs | self._kwargs, func=func
        )

        return await func(packet, **kwargs)

    def resolve_router(self, packet: type[Packet]) -> Handler | None:
        packet_id = (packet.__state__, packet.packet_id)

        if packet_id in self._commands:
            return self._commands[packet_id]
        return None
