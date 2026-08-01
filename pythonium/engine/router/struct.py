import inspect
from typing import TYPE_CHECKING, Any

from pythonium.engine.typealiases import Handler
from pythonium.registries.base import Registry

if TYPE_CHECKING:
    from pythonium.engine.client import Client
    from pythonium.engine.server.di import Container


class HandlerStruct:
    """Struct for storing handler and its kwargs."""

    def __init__(self, func: Handler) -> None:
        self.func = func

        self.needed_params = frozenset(
            inspect.signature(self.func).parameters.keys()
        )

    async def __call__(
        self,
        *args: Any,  # noqa: ANN401
        container: Container,
        client: Client | None = None,
    ) -> None | Registry:
        """Get handler with partial kwargs."""
        kwargs = container.resolve_kwargs(self.needed_params, client=client)

        return await self.func(*args, **kwargs)
