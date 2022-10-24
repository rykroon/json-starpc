import typing

from starlette.background import BackgroundTask
from starlette.endpoints import HTTPEndpoint, WebSocketEndpoint
from starlette.responses import Response
from starlette.requests import Request
from starlette.websockets import WebSocket

from jsonstarpc.exceptions import ParseError
from jsonstarpc.responses import SuccessResponse
from jsonstarpc.utils import parse_json, get_function, validate_request


class JsonRpcHttpEndpoint(HTTPEndpoint):

    async def post(self, http_request: Request) -> typing.Any:
        if http_request.headers.get('content-type') != 'application/json':
            raise ParseError("Invalid ContentType.")
            # return Response(status_code=415)

        raw_data = await http_request.body()
        json_data = parse_json(raw_data)
        request = validate_request(json_data)
        function = get_function(http_request, request.method)

        # notification
        if request.id is None:
            task = BackgroundTask(function, request.params)
            return Response(status_code=202, background=task)

        result = await function(request.params)

        return SuccessResponse(result, id=request.id)


class JsonRpcWebsocketEndpoint(WebSocketEndpoint):

    encoding = 'text'

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        json_data = parse_json(data)
        request = validate_request(json_data)
        function = get_function(websocket, request.method)
        result = await function(request.params)

        if request.id is None:
            return

        await websocket.send_json({
            'jsonrpc': '2.0',
            'result': result,
            'id': request.id
        })
