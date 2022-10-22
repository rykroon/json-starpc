from typing import Any, Optional
from starlette.responses import JSONResponse


class SuccessResponse(JSONResponse):

    def __init__(
        self,
        result: Any,
        *,
        jsonrpc: str = "2.0",
        id: Optional[str | int] = None,
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
        error: dict,
        *,
        jsonrpc: str = "2.0",
        id: Optional[str | int] = None,
        **kwargs
    ):
        super().__init__({
            'jsonrpc': jsonrpc,
            'error': error,
            'id': id
        }, **kwargs)
