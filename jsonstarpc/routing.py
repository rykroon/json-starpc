from starlette.routing import Route, WebSocketRoute
from starlette.types import Scope, Send, Receive
from jsonstarpc.endpoints import JsonRpcHttpEndpoint, JsonRpcWebsocketEndpoint
from jsonstarpc.functions import Function


class JsonRpcRoute(Route):

    def __init__(
        self,
        path: str,
        *,
        functions: list[Function] | None = None,
        name: str | None = None,
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

    async def handle(self, scope: Scope, receive: Receive, send: Send) -> None:
        scope['functions'] = self.functions
        await super().handle(scope, receive, send)


class JsonRpcWebsocketRoute(WebSocketRoute):

    def __init__(
        self,
        path: str,
        *,
        functions: list[Function] | None = None,
        name: str | None = None
    ):
        super().__init__(
            path,
            JsonRpcWebsocketEndpoint,
            name=name
        )

        self.functions = [] if functions is None else list(functions)

    async def handle(self, scope: Scope, receive: Receive, send: Send) -> None:
        scope['functions'] = self.functions
        await super().handle(scope, receive, send)
