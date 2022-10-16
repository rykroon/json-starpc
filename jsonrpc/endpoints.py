import json

from starlette.background import BackgroundTask
from starlette.endpoints import HTTPEndpoint, WebSocketEndpoint
from starlette.responses import Response, JSONResponse

from jsonrpc.exceptions import ParseError, MethodNotFound
from jsonrpc.validation import validate_request


class JsonRpcEndpointMixin:

    def parse_json(self, raw_data: bytes):
        try:
            return json.loads(raw_data)

        except json.JSONDecodeError as e:
            raise ParseError(str(e))


class JsonRpcHttpEndpoint(HTTPEndpoint, JsonRpcEndpointMixin):

    async def post(self, http_request):
        if http_request.headers.get('content-type') != 'application/json':
            return Response(status_code=415)

        raw_data = await http_request.body()
        request = self.parse_json(raw_data)

        validate_request(request)

        functions = http_request.scope['functions']

        for function in functions:
            if function.name == request['method']:
                break
        else:
            raise MethodNotFound

        ba = function.get_bound_arguments(request.get('params'))

        # notification
        if 'id' not in request:
            task = BackgroundTask(function, *ba.args, **ba.kwargs)
            return Response(status_code=202, background=task) 

        result = await function(*ba.args, **ba.kwargs)

        response = {
            'jsonrpc': "2.0",
            'id': request['id'],
            'result': result
        }

        return JSONResponse(response)




class JsonRpcWebsocketEndpoint(WebSocketEndpoint):
    ...