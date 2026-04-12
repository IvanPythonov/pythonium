import inspect
from typing import Any

from pythonium.engine.typealiases import Handler


class HandlerStruct:
    """Struct for storing handler and its kwargs."""

    def __init__(self, func: Handler, kwargs: dict[str, Any]) -> None:
        self.func = func

        self._kwargs_signature = self._get_func_params()

        self.needs_client = "client" in self._kwargs_signature

        self.kwargs = {
            k: v for k, v in kwargs.items() if k in self._kwargs_signature
        }

    async def __call__(self, *args: Any, **dynamic_kwargs: Any) -> None:  # noqa: ANN401
        """Get handler with partial kwargs."""
        to_pass = {}

        if self.needs_client:
            to_pass["client"] = dynamic_kwargs["client"]

        return await self.func(*args, **self.kwargs, **to_pass)

    def _get_func_params(self) -> frozenset[str]:
        """Get kwargs and return frozenset."""
        return frozenset(inspect.signature(self.func).parameters.keys())
