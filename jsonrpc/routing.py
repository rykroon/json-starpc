from typing import Optional, List

from starlette.routing import Route, WebSocketRoute
from jsonrpc.endpoints import JsonRpcHttpEndpoint, JsonRpcWebsocketEndpoint
from jsonrpc.functions import Function


class JsonRpcRoute(Route):

    def __init__(
        self,
        path: str,
        *,
        functions: Optional[List[Function]] = None,
        name: Optional[str] = None,
        include_in_schema: bool = True
    ):
        super().__init__(
            path,
            JsonRpcHttpEndpoint,
            methods=['POST'],
            name=name,
            include_in_schema=include_in_schema
        )

        self.functions = [] if functions is None else list(functions)

    async def handle(self, scope, receive, send):
        scope['functions'] = self.functions
        await super().handle(scope, receive, send)


class JsonRpcWebsocketRoute(WebSocketRoute):

    def __init__(
        self,
        path: str,
        *,
        functions: Optional[List[Function]] = None,
        name: Optional[str] = None
    ):
        super().__init__(
            path,
            JsonRpcWebsocketEndpoint,
            name=name
        )

        self.functions = [] if functions is None else list(functions)

    async def handle(self, scope, receive, send):
        scope['functions'] = self.functions
        await super().handle(scope, receive, send)
