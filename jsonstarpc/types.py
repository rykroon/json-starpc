import typing as t


class _JsonRpc(t.TypedDict):
    jsonrpc: str


class _JsonRpcRequestRequired(_JsonRpc):
    method: str


class JsonRpcRequest(_JsonRpcRequestRequired, total=False):
    params: dict[str, t.Any] | list[t.Any]
    id: str | int


class _JsonRpcResponse(_JsonRpc):
    id: str | int | None


class JsonRpcSuccessResponse(_JsonRpcResponse):
    result: t.Any


class _JsonRpcErrorRequired(t.TypedDict):
    code: int
    message: str


class JsonRpcError(_JsonRpcErrorRequired, total=False):
    data: dict[str, t.Any]


class JsonRpcErrorResponse(_JsonRpcResponse):
    error: JsonRpcError
