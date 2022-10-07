import json
import logging

from starlette.background import BackgroundTasks
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

        if isinstance(json_data, dict):
            raw_requests = [json_data]

        elif isinstance(json_data, list):
            raw_requests = [obj for obj in json_data]

        requests = []
        responses = []
        for request in raw_requests:
            request, error = validate_request(request)

            if error is not None:
                response = error_to_response(error)
                responses.append(response)
                continue

            requests.append(request)

        tasks = BackgroundTasks()
        for request in requests:
            # notification
            if 'id' not in request:
                tasks.add_task(self.method_router.dispatch, request)
                continue

            response, error = await self.method_router.dispatch(request)

            if error is not None:
                response = error_to_response(error, id=request['id'])

            responses.append(response)

        if not responses:
            return Response(status_code=204, background=tasks)

        return JSONResponse(responses, background=tasks)

    @websocket_session
    async def websocket_flow(self, websocket):
        await websocket.accept()
        while True:
            ...



            
    

        