import typing
from jsonstarpc.exceptions import InvalidRequest


def validate_request(request: dict[str, typing.Any]) -> None:
    if not isinstance(request, dict):
        raise InvalidRequest('Request must be an object.')

    if 'jsonrpc' not in request:
        raise InvalidRequest("Missing member 'jsonrpc'.")

    if not isinstance(request['jsonrpc'], str):
        raise InvalidRequest("Member 'jsonrpc' must be a 'string'.")

    if request['jsonrpc'] != "2.0":
        raise InvalidRequest("Member 'jsonrpc' must be '2.0'.")

    if 'method' not in request:
        raise InvalidRequest("Missing member 'method'.")

    if not isinstance(request['method'], str):
        raise InvalidRequest("Member 'method' must be a 'string'.")

    if 'params' in request:
        if not isinstance(request['params'], list | dict):
            raise InvalidRequest(
                "Member 'params' must be an 'array' or an 'object'."
            )

    if 'id' in request:
        if not isinstance(request['id'], str | int):
            raise InvalidRequest("Member 'id' must be a 'string' or 'number'.")


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
