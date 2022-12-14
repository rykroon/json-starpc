import typing


class JsonRpcException(Exception):
    code: int
    message: str
    data: dict[str, typing.Any] | None

    def __init__(self, message: str | None = None, /, **data: typing.Any):
        if message is not None:
            self.message = message
        self.data = data if data else None


class ParseError(JsonRpcException):
    code = -32700
    message = "Parse error."


class InvalidRequest(JsonRpcException):
    code = -32600
    message = "Invalid request."


class MethodNotFound(JsonRpcException):
    code = -32601
    message = "Method not found."


class InvalidParams(JsonRpcException):
    code = -32602
    message = "Invalid params."


class InternalError(JsonRpcException):
    code = -32603
    message = "Internal error."
