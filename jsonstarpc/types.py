from typing import Any, Literal, NotRequired, Required, TypedDict


class JsonRpcRequest(TypedDict):
    jsonrpc: Required[Literal['2.0']]
    method: Required[str]
    params: NotRequired[dict[str, Any] | list[Any]]
    id: NotRequired[str | int]


class JsonRpcSuccessResponse(TypedDict):
    jsonrpc: Required[Literal['2.0']]
    result: Required[Any]
    id: Required[str | int | None]


class JsonRpcError(TypedDict):
    code: Required[int]
    message: Required[str]
    data: NotRequired[dict[str, Any]]


class JsonRpcErrorResponse(TypedDict):
    jsonrpc: Required[Literal['2.0']]
    error: Required[JsonRpcError]
    id: Required[str | int | None]
