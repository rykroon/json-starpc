import inspect
from typing import Callable


from jsonrpc.errors import invalid_params, method_not_found
from jsonrpc.utils import exception_to_error, error_to_response


class Method:
    def __init__(self, func: Callable, name: str = None):
        self.func = func
        self.signature = inspect.signature(self.func)
        self.name = name if name is not None else func.__name__

    async def __call__(self, request) -> tuple[dict | None, dict | None]:
        try:
            if 'params' not in request:
                ba = self.signature.bind()
            
            elif isinstance(request['params'], list):
                ba = self.signature.bind(*request['params'])

            elif isinstance(request['params'], dict):
                ba = self.signature.bind(**request['params'])

        except TypeError as e:
            return None, invalid_params(str(e))

        result = await self.func(*ba.args, **ba.kwargs)

        return {
            'jsonrpc': "2.0",
            'id': request['id'],
            'result': result
        }, None


class MethodRouter:

    def __init__(self, methods=None):
        self.methods = [] if methods is None else list(methods)

    async def dispatch(self, request: dict):
        for method in self.methods:
            if method.name != request['method']:
                continue

            try:
                return await method(request)
            
            except Exception as e:
                error = exception_to_error(e)
                id = request['id'] if 'id' in request else None
                response = error_to_response(error, id=id)
                return response

        return None, method_not_found()
