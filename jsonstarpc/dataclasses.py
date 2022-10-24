from dataclasses import dataclass
import typing


@dataclass
class JsonRpcRequest:
    jsonrpc: str
    method: str
    params: dict[str, typing.Any] | list[typing.Any] | None = None
    id: str | int | None = None


@dataclass
class JsonRpcSuccessResponse:
    jsonrpc: str
    result: typing.Any
    id: str | int | None = None


@dataclass
class JsonRpcError:
    code: int
    message: str
    data: dict[str, typing.Any] | None = None


@dataclass
class JsonRpcErrorResponse:
    jsonrpc: str
    error: JsonRpcError
    id: str | int | None = None
