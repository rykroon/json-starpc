import inspect
from typing import Callable

from starlette.routing import BaseRoute, Match
from starlette.types import Scope

from jsonrpc.exceptions import InvalidParams, MethodNotFound


class Method(BaseRoute):
    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func
        self.signature = inspect.signature(self.func)

    async def matches(self, scope: Scope) -> tuple[Match, Scope]:
        request = scope['jsonrpc']['request']
        if request.method == self.name:
            return Match.FULL, {}
        return Match.NONE, {}

    async def handle(self, scope, receive, send):
        request = scope['jsonrpc']['request']
        try:
            if not request.params:
                ba = self.signature.bind()
            
            elif isinstance(request.params, list):
                ba = self.signature.bind(*request.params)

            elif isinstance(request.params, dict):
                ba = self.signature.bind(**request.params)

        except TypeError as e:
            raise InvalidParams(e)

        try:
            result = await self.func(*ba.args, **ba.kwargs)
            error = None
        
        except Exception as e:
            result = None
            error = {
                'code': 0,
                'message': str(e)
            }

        response = {'jsonrcpc': "2.0"}
        if error is not None:
            response['error'] = error
        else:
            response['result'] = result

        scope['jsonrpc']['response'] = response


class Router:
    def __init__(self, methods=None):
        self.methods = [] if methods is None else list(methods)

    async def __call__(self, scope, send, receive):
        for method in self.methods:
            match, child_scope = method.matches(scope)
            if match == Match.FULL:
                scope.update(child_scope)
                await method.handle(scope, receive, send)

        raise MethodNotFound