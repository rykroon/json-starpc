from starlette.responses import JSONResponse


class SuccessResponse(JSONResponse):

    def __init__(self, result, *, jsonrpc="2.0", id=None, **kwargs):
        super().__init__({
            'jsonrpc': jsonrpc,
            'result': result,
            'id': id
        }, **kwargs)


class ErrorResponse(JSONResponse):
    def __init__(self, error: dict, *, jsonrpc="2.0", id=None, **kwargs):
        super().__init__({
            'jsonrpc': jsonrpc,
            'error': error,
            'id': id
        }, **kwargs)
