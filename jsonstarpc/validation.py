import typing
from jsonstarpc.exceptions import InvalidRequest
from jsonstarpc.dataclasses import JsonRpcRequest


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


def validate_error(error: dict[str, typing.Any]) -> None:
    assert isinstance(error, dict)

    assert 'code' in error
    assert isinstance(error['code'], int)

    assert 'message' in error
    assert isinstance(error['message'], str)

    if 'data' in error:
        assert isinstance(error['data'], dict)

    allowed_fields = ('code', 'message', 'data')
    for key in error:
        assert key in allowed_fields


def validate_response(response: dict[str, typing.Any]) -> None:
    assert isinstance(response, dict)

    assert 'jsonrpc' in response
    assert isinstance(response['jsonrpc'], str)
    assert response['jsonrpc'] == '2.0'

    assert ('result' in response) ^ ('error' in response)

    if 'error' in response:
        validate_error(response['error'])

    assert 'id' in response
    assert isinstance(response['id'], str | int | None)

    allowed_fields = ('jsonrpc', 'result', 'error', 'id')
    for key in response:
        assert key in allowed_fields
