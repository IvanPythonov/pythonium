import logging
from collections.abc import Callable
from typing import Any, Self

from pythonium.engine.enums.states import State
from pythonium.engine.exceptions import PacketNotHandledError
from pythonium.engine.packets.base import Packet
from pythonium.engine.router.struct import HandlerStruct
from pythonium.engine.typealiases import Handler

logger = logging.getLogger(__name__)


class Router:
    """Router can route updates."""

    def __init__(
        self, *, name: str | None = None, **kwargs: dict[str, Any]
    ) -> None:
        self.name = name or hex(id(self))

        self._parent_router: Router | None = None
        self.sub_routers: list[Router] = []

        self._unbaked_handlers: dict[type[Packet], Handler] = {}
        self._baked_handlers: dict[tuple[State, int], HandlerStruct] = {}

        self._kwargs = kwargs

    def on(self, *packets: type[Packet]) -> Callable[[Handler], Handler]:
        def decorator(
            func: Handler,
        ) -> Handler:
            for packet in packets:
                self._unbaked_handlers[packet] = func
            return func

        return decorator

    @property
    def handlers(self) -> dict[tuple[State, int], HandlerStruct]:
        return self._baked_handlers

    @property
    def unbaked_handlers(self) -> dict[type[Packet], Handler]:
        return self._unbaked_handlers

    @property
    def all_commands(self) -> dict[tuple[State, int], HandlerStruct]:
        """Get all commands from this router and sub-routers."""
        commands = self._baked_handlers.copy()
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

    def include_router(self, router: "Router") -> "Router":
        """Attach another router."""
        if not isinstance(router, Router):
            msg = (
                "router should be instance of "
                f"Router not {type(router).__class__.__name__}"
            )
            raise TypeError(msg)

        router.parent_router = self
        self._unbaked_handlers.update(router.unbaked_handlers)

        return self

    def bake(self, **static_kwargs: Any) -> None:  # noqa: ANN401
        """Bake handlers, resolving kwargs."""
        for packet, func in self._unbaked_handlers.items():
            handler_struct = HandlerStruct(func=func, kwargs=static_kwargs)

            self._baked_handlers[(packet.state, packet.packet_id)] = (
                handler_struct
            )
        logger.info(
            "Baking complete: %s handlers registered",
            len(self._baked_handlers),
        )

        pretty_printed_handlers = []  # packet name -> handler name
        for (state, packet_id), handler_struct in self._baked_handlers.items():
            handler_name = handler_struct.func.__name__
            pretty_printed_handlers.append(
                f"{state}, {packet_id:#04x} -> {handler_name}"
            )
        logger.debug("Baked handlers: %s", pretty_printed_handlers)

    async def route(self, packet: Packet, **kwargs: object) -> None:
        """Route command to appropriate handler."""
        handler_struct = self.resolve_router(packet=type(packet))

        if handler_struct is None:
            raise PacketNotHandledError(
                packet_name=type(packet).__name__,
            )

        return await handler_struct(packet, **kwargs)

    def resolve_router(self, packet: type[Packet]) -> HandlerStruct | None:
        packet_id = (packet.state, packet.packet_id)

        if packet_id in self._baked_handlers:
            return self._baked_handlers[packet_id]
        return None
