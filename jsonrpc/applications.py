import json
import logging

from starlette.background import BackgroundTask
from starlette.responses import JSONResponse, Response
from starlette.routing import request_response, websocket_session

from jsonrpc.errors import parse_error
from jsonrpc.methods import MethodRouter
from jsonrpc.utils import method_decorator, error_to_response
from jsonrpc.validation import validate_request


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.INFO)


request_response = method_decorator(request_response)
websocket_session = method_decorator(websocket_session)


class JsonRpc:

    def __init__(self, methods=None, path=None):
        self.method_router = MethodRouter(methods)
        self.path = path

    async def __call__(self, scope, receive, send):
        if scope['path'] != self.path:
            ...

        if scope['type'] == 'http':
            await self.http_flow(scope, receive, send)

        if scope['type'] == 'websocket':
            await self.websocket_flow(scope, receive, send)

    def parse_json(self, data: bytes):
        try:
            return json.loads(data), None

        except json.JSONDecodeError as e:
            return None, parse_error()

    @request_response
    async def http_flow(self, http_request):
        if http_request.method != 'POST':
            return Response(status_code=405)

        if http_request.headers.get('content-type') != 'application/json':
            return Response(status_code=415)

        raw_data = await http_request.body()
        json_data, error = self.parse_json(raw_data)
        if error is not None:
            response = error_to_response(error)
            return JSONResponse(response, status_code=400)

        request, error = validate_request(json_data)
        if error is not None:
            response = error_to_response(error)
            return JSONResponse(response, status_code=400)

        # notification
        if 'id' not in request:
            task = BackgroundTask(self.method_router.dispatch, request)
            return Response(status_code=204, background=task) 

        response, error = await self.method_router.dispatch(request)
        if error is not None:
            response = error_to_response(error, id=request['id'])

        return JSONResponse(response)

    @websocket_session
    async def websocket_flow(self, websocket):
        await websocket.accept()
        while True:
            ...



            
    

        