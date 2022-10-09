import inspect
from typing import Callable

from starlette.routing import get_name
from jsonrpc.exceptions import InvalidParams, MethodNotFound


class Function:
    def __init__(self, func: Callable, *, name: str = None):
        self.func = func
        self.signature = inspect.signature(self.func)
        self.name = get_name(func) if name is None else name

    async def __call__(self, *args, **kwargs):
        return await self.func(*args, **kwargs)

    def get_bound_arguments(self, params):
        try:
            if params is None:
                return self.signature.bind()

            elif isinstance(params, list):
                return self.signature.bind(*params)

            elif isinstance(params, dict):
                return self.signature.bind(**params)

        except TypeError as e:
            raise InvalidParams(str(e))

