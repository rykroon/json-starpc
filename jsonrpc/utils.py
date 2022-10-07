from functools import wraps


def method_decorator(decorator):
    def new_decorator(unbound_method):
        @wraps(unbound_method)
        def wrapper(self, *args, **kwargs):
            bound_method = unbound_method.__get__(self)
            decorated_method = decorator(bound_method)
            return decorated_method(*args, **kwargs)
        return wrapper
    return new_decorator


def is_notification(request: dict):
    return 'id' in request


def exception_to_error(exc):
    return {
        'code': 0,
        'message': str(exc)
    }


def error_to_response(error: dict, id=None) -> dict:
    return {
        'jsonrpc': "2.0",
        'error': error,
        'id': id
    }
