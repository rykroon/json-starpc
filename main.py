import logging

from starlette.applications import Starlette

from jsonrpc.exceptions import JsonRpcException
from jsonrpc.functions import Function
from jsonrpc.responses import ErrorResponse
from jsonrpc.routing import JsonRpcRoute, JsonRpcWebsocketRoute


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.INFO)


async def add(x: int, y: int) -> int:
    logger.info("add")
    return x + y


functions = [
    Function(add)
]

routes = [
    JsonRpcRoute('/', functions=functions),
    JsonRpcWebsocketRoute('/ws', functions=functions)
]


async def jsonrpc_error(request, exc):
    return ErrorResponse(
        error_code=exc.code,
        error_message=exc.message
    )

async def exception_handler(request, exc):
    return ErrorResponse(
        error_code=0,
        error_message=str(exc)
    )


exception_handlers = {
    Exception: exception_handler,
    JsonRpcException: jsonrpc_error
}


app = Starlette(
    #debug=True,
    routes=routes,
    exception_handlers=exception_handlers
)
