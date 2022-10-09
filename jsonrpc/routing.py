from starlette.routing import Route, WebSocketRoute
from jsonrpc.endpoints import JsonRpcHttpEndpoint


class JsonRpcRoute(Route):
    
    def __init__(self, path, *, functions=None, name=None, include_in_schema=True):
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
    ...
