from functools import wraps
import inspect

from jsonstarpc.dataclasses import JsonRpcError
from jsonstarpc.exceptions import JsonRpcException


def catch_jsonrpc_exception(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            if inspect.isawaitable(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)

        except JsonRpcException as e:
            return JsonRpcError(
                code=e.code,
                message=e.message,
                data=e.data
            )
    return wrapper
