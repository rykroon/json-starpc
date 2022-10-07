import inspect
from typing import Callable


from jsonrpc.exceptions import InvalidParams, MethodNotFound
from jsonrpc.utils import exception_to_error, error_to_response


class Method:
    def __init__(self, func: Callable, name: str = None):
        self.func = func
        self.signature = inspect.signature(self.func)
        self.name = name if name is not None else func.__name__

    async def __call__(self, request: dict):
        try:
            if 'params' not in request:
                ba = self.signature.bind()
            
            elif isinstance(request['params'], list):
                ba = self.signature.bind(*request['params'])

            elif isinstance(request['params'], dict):
                ba = self.signature.bind(**request['params'])

        except TypeError as e:
            raise InvalidParams(str(e))

        return await self.func(*ba.args, **ba.kwargs)


class MethodRouter:

    def __init__(self, methods=None):
        self.methods = [] if methods is None else list(methods)

    async def dispatch(self, request: dict):
        for method in self.methods:
            if method.name != request['method']:
                continue
            return await method(request)
        raise MethodNotFound
