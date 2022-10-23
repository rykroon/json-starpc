import json
import typing

from starlette.background import BackgroundTask
from starlette.endpoints import HTTPEndpoint, WebSocketEndpoint
from starlette.responses import Response
from starlette.requests import HTTPConnection, Request
from starlette.websockets import WebSocket


from jsonrpc.exceptions import ParseError, MethodNotFound
from jsonrpc.functions import Function
from jsonrpc.responses import SuccessResponse
from jsonrpc.validation import validate_request


class JsonRpcEndpointMixin:

    def parse_json(self, raw_data: bytes):
        try:
            return json.loads(raw_data)

        except json.JSONDecodeError as e:
            raise ParseError(str(e))

    def get_function(
        self,
        connection: HTTPConnection,
        method: str
    ) -> Function:

        functions: list[Function] = connection.scope['functions']

        for function in functions:
            if function.name == method:
                return function

        raise MethodNotFound


class JsonRpcHttpEndpoint(HTTPEndpoint, JsonRpcEndpointMixin):

    async def post(self, http_request: Request) -> typing.Any:
        if http_request.headers.get('content-type') != 'application/json':
            return Response(status_code=415)

        raw_data = await http_request.body()
        request = self.parse_json(raw_data)

        validate_request(request)

        function = self.get_function(http_request, request['method'])

        # notification
        if 'id' not in request:
            task = BackgroundTask(function, request.get('params'))
            return Response(status_code=202, background=task)

        result = await function(request.get('params'))

        return SuccessResponse(result, id=request['id'])


class JsonRpcWebsocketEndpoint(WebSocketEndpoint, JsonRpcEndpointMixin):

    encoding = 'text'

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        request = self.parse_json(data)

        validate_request(request)

        function = self.get_function(websocket, request['method'])

        result = await function(request.get('params'))

        if 'id' not in request:
            return

        await websocket.send_json({
            'jsonrpc': '2.0',
            'result': result,
            'id': request['id']
        })
