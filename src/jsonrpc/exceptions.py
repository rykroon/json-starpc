

class JsonRpcException(Exception):
    code = None

    def __init__(self, message, /, **kwargs):
        self.message = message
        self.data = kwargs


class ParseError(JsonRpcException):
    code = 32700


class InvalidRequest(JsonRpcException):
    code = 32600


class MethodNotFound(JsonRpcException):
    code = 32601


class InvalidParams(JsonRpcException):
    code = 32602


class InternalError(JsonRpcException):
    code = 32603


