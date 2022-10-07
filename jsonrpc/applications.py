import json
import logging

from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse, Response
from starlette.routing import Route, WebSocketRoute

from jsonrpc.exceptions import ParseError
from jsonrpc.methods import MethodRouter
from jsonrpc.validation import validate_request


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.INFO)


class JsonRpc(Starlette):

    def __init__(
        self,
        methods=None,
        path='/',
        debug: bool = False,
        middleware=None,
        exception_handlers=None,
        on_startup=None,
        on_shutdown=None,
        lifespan=None
    ) -> None:

        routes=[
            Route(path, http_flow, methods=['POST']),
            WebSocketRoute(path, websocket_flow)
        ]

        super().__init__(
            debug=debug,
            routes=routes,
            middleware=middleware,
            exception_handlers=exception_handlers,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan
        )

        self.method_router = MethodRouter(methods)

    def parse_json(self, data: bytes):
        try:
            return json.loads(data)

        except json.JSONDecodeError as e:
            raise ParseError


async def http_flow(http_request):
    app = http_request.app

    if http_request.headers.get('content-type') != 'application/json':
        return Response(status_code=415)

    raw_data = await http_request.body()
    request = app.parse_json(raw_data)

    validate_request(request)

    # notification
    if 'id' not in request:
        task = BackgroundTask(app.method_router.dispatch, request)
        return Response(status_code=202, background=task) 

    result = await app.method_router.dispatch(request)

    response = {
        'jsonrpc': "2.0",
        'id': request['id'],
        'result': result
    }

    return JSONResponse(response)


async def websocket_flow(websocket):
    await websocket.accept()
    while True:
        ...
            
    

        