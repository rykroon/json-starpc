from jsonrpc.errors import invalid_request


def validate_request(request: dict) -> tuple[dict | None, dict | None]:
    if not isinstance(request, dict):
        return None, invalid_request('Request must be an object.')

    if 'jsonrpc' not in request:
        return None, invalid_request("Missing member 'jsonrpc'.")

    if not isinstance(request['jsonrpc'], str):
        return None, invalid_request("Member 'jsonrpc' must be a 'string'.")

    if request['jsonrpc'] != "2.0":
        return None, invalid_request("Member 'jsonrpc' must be '2.0'.")

    if 'method' not in request:
        return None, invalid_request("Missing member 'method'.")

    if not isinstance(request['method'], str):
        return None, invalid_request("Member 'method' must be a 'string'.")

    if 'params' in request:
        if not isinstance(request['params'], list | dict):
            return None, invalid_request("Member 'params' must be an 'array' or an 'object'.")

    if 'id' in request:
        if not isinstance(request['id'], str | int):
            return None, invalid_request("Member 'id' must be a 'string' or 'number'.")

    return request, None


def validate_error(error: dict):
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


def validate_response(response: dict):
    assert isinstance(response, dict)

    assert 'jsonrpc' in response
    assert isinstance(response['jsonrpc'], str)
    assert response['jsonrpc'] == '2.0'

    assert 'result' in response ^ 'error' in response

    if 'error' in response:
        validate_error(response['error'])

    assert 'id' in response
    assert isinstance(response['id'], str | int | None)

    allowed_fields = ('jsonrpc', 'result', 'error', 'id')
    for key in response:
        assert key in allowed_fields
