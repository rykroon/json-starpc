import inspect
from typing import Any, Callable

from starlette.routing import get_name
from jsonrpc.exceptions import InvalidParams


class Function:
    def __init__(self, func: Callable[..., Any], *, name: str | None = None):
        self.func = func
        self.signature = inspect.signature(self.func)
        self.name = get_name(func) if name is None else name

    async def __call__(
        self,
        params: dict[str, Any] | list[Any] | None = None,
        /
    ) -> Any:
        ba = self._get_bound_arguments(params)
        return await self.func(*ba.args, **ba.kwargs)

    def _get_bound_arguments(
        self,
        params: dict[str, Any] | list[Any] | None
    ) -> inspect.BoundArguments:
        try:
            if params is None:
                return self.signature.bind()

            elif isinstance(params, list):
                return self.signature.bind(*params)

            elif isinstance(params, dict):
                return self.signature.bind(**params)

        except TypeError as e:
            raise InvalidParams(str(e))
