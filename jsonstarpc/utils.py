import json
import typing

from starlette.requests import HTTPConnection

from jsonstarpc.dataclasses import JsonRpcRequest
from jsonstarpc.exceptions import InvalidRequest, ParseError, MethodNotFound
from jsonstarpc.functions import Function


def parse_json(raw_data: str | bytes) -> typing.Any:
    try:
        return json.loads(raw_data)

    except json.JSONDecodeError as e:
        raise ParseError(str(e))


def get_function(
    connection: HTTPConnection,
    method: str
) -> Function:

    functions: list[Function] = connection.scope['functions']

    for function in functions:
        if function.name == method:
            return function

    raise MethodNotFound


def validate_request(data: typing.Any) -> JsonRpcRequest:
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

    if 'params' in data:
        if not isinstance(data['params'], list | dict):
            raise InvalidRequest(
                "Member 'params' must be an 'array' or an 'object'."
            )

    if 'id' in data:
        if not isinstance(data['id'], str | int):
            raise InvalidRequest("Member 'id' must be a 'string' or 'number'.")

    return JsonRpcRequest(
        jsonrpc=data['jsonrpc'],
        method=data['method'],
        params=data.get('params'),
        id=data.get('id')
    )
