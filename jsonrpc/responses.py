import typing
from starlette.responses import JSONResponse


class SuccessResponse(JSONResponse):

    def __init__(
        self,
        result: typing.Any,
        *,
        jsonrpc: str = "2.0",
        id: str | int | None = None,
        **kwargs
    ):
        super().__init__({
            'jsonrpc': jsonrpc,
            'result': result,
            'id': id
        }, **kwargs)


class ErrorResponse(JSONResponse):
    def __init__(
        self,
        error: dict[str, typing.Any],
        *,
        jsonrpc: str = "2.0",
        id: str | int | None = None,
        **kwargs
    ):
        super().__init__({
            'jsonrpc': jsonrpc,
            'error': error,
            'id': id
        }, **kwargs)
