

def make_error(code:int, message: str, **data):
    error = {
        'code': code,
        'message': message
    }
    if data:
        error['data'] = data
    return error


def parse_error(message=None, /, **data):
    message = 'Parse error.' if message is None else message
    return make_error(32700, message, **data)


def invalid_request(message=None, **data):
    message = 'Invalid request.' if message is None else message
    return make_error(32600, message, **data)


def method_not_found(message=None, /, **data):
    message = "Method not found." if message is None else message
    return make_error(32601, message, **data)


def invalid_params(message=None, /, **data):
    message = "Invalid params." if message is None else message
    return make_error(32602, message, **data) 


def internal_error(message=None, /, **data):
    message = "Internal error." if message is None else message
    return make_error(32603, message, **data)

