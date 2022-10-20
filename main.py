import asyncio
import logging

from starlette.applications import Starlette
from starlette.responses import JSONResponse

from jsonrpc.exceptions import JsonRpcException
from jsonrpc.functions import Function
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
    return JSONResponse({
        'jsonrpc': "2.0",
        'error': {
            'code': exc.code,
            'message': exc.message,
        }
    })

async def exception_handler(request, exc):
    return JSONResponse({
        'jsonrpc': "2.0",
        'error': {
            'code': 0,
            'message': str(exc),
        }
    })


exception_handlers = {
    Exception: exception_handler,
    JsonRpcException: jsonrpc_error
}


app = Starlette(
    #debug=True,
    routes=routes,
    exception_handlers=exception_handlers
)
