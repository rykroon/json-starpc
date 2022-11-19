import inspect
import typing as t

from starlette.routing import get_name
from jsonstarpc.exceptions import InvalidParams


class Function:
    def __init__(self, func: t.Callable[..., t.Any], *, name: str | None = None):
        self.func = func
        self.signature = inspect.signature(self.func)
        self.name = get_name(func) if name is None else name

    async def __call__(
        self,
        params: dict[str, t.Any] | list[t.Any] | None = None,
        /
    ) -> t.Any:
        ba = self._get_bound_arguments(params)
        if inspect.iscoroutinefunction(self.func):
            return await self.func(*ba.args, **ba.kwargs)
        return self.func(*ba.args, **ba.kwargs)

    def _get_bound_arguments(
        self,
        params: dict[str, t.Any] | list[t.Any] | None
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

        raise TypeError
