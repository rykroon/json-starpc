import json

from starlette.background import BackgroundTask
from starlette.endpoints import HTTPEndpoint, WebSocketEndpoint
from starlette.responses import Response

from jsonrpc.exceptions import ParseError, MethodNotFound
from jsonrpc.responses import SuccessResponse
from jsonrpc.validation import validate_request


class JsonRpcEndpointMixin:

    def parse_json(self, raw_data: bytes):
        try:
            return json.loads(raw_data)

        except json.JSONDecodeError as e:
            raise ParseError(str(e))

    def get_function(self, connection, method):
        functions = connection.scope['functions']

        for function in functions:
            if function.name == method:
                return function

        raise MethodNotFound


class JsonRpcHttpEndpoint(HTTPEndpoint, JsonRpcEndpointMixin):

    async def post(self, http_request):
        if http_request.headers.get('content-type') != 'application/json':
            return Response(status_code=415)

        raw_data = await http_request.body()
        request = self.parse_json(raw_data)

        validate_request(request)

        function = self.get_function(http_request, request['method'])

        ba = function.get_bound_arguments(request.get('params'))

        # notification
        if 'id' not in request:
            task = BackgroundTask(function, *ba.args, **ba.kwargs)
            return Response(status_code=202, background=task) 

        result = await function(*ba.args, **ba.kwargs)

        return SuccessResponse(result, id=request['id'])


class JsonRpcWebsocketEndpoint(WebSocketEndpoint, JsonRpcEndpointMixin):

    encoding = 'text'
    
    async def on_receive(self, websocket, data):
        request = self.parse_json(data)

        validate_request(request)

        function = self.get_function(websocket, request['method'])
        ba = function.get_bound_arguments(request.get('params'))

        result = await function(*ba.args, **ba.kwargs)

        if 'id' not in request:
            return

        await websocket.send_json({
            'jsonrpc': '2.0',
            'result': result,
            'id': request['id']
        })
