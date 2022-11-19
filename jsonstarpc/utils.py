import json
import typing as t

from jsonstarpc.types import JsonRpcRequest
from jsonstarpc.exceptions import InvalidRequest, ParseError, MethodNotFound
from jsonstarpc.functions import Function


def parse_json(raw_data: str | bytes) -> t.Any:
    try:
        return json.loads(raw_data)

    except json.JSONDecodeError as e:
        raise ParseError(str(e))


def get_function(method: str, functions: list[Function]) -> Function:
    for function in functions:
        if function.name == method:
            return function
    raise MethodNotFound


def validate_request(data: t.Any) -> JsonRpcRequest:
    if not isinstance(data, dict):
        raise InvalidRequest('Request must be an object.')

    if 'jsonrpc' not in data:
        raise InvalidRequest("Missing member 'jsonrpc'.")

    if not isinstance(data['jsonrpc'], str):
        raise InvalidRequest("Member 'jsonrpc' must be a 'string'.")

    if data['jsonrpc'] != "2.0":
        raise InvalidRequest("Member 'jsonrpc' must be '2.0'.")

    if 'method' not in data:
        raise InvalidRequest("Missing member 'method'.")

    if not isinstance(data['method'], str):
        raise InvalidRequest("Member 'method' must be a 'string'.")

    request: JsonRpcRequest = {
        'jsonrpc': data['jsonrpc'],
        'method': data['method']
    }

    if 'params' in data:
        if not isinstance(data['params'], list | dict):
            raise InvalidRequest(
                "Member 'params' must be an 'array' or an 'object'."
            )
        request['params'] = data['params']

    if 'id' in data:
        if not isinstance(data['id'], str | int):
            raise InvalidRequest("Member 'id' must be a 'string' or 'number'.")
        request['id'] = data['id']

    return request
