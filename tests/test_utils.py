import pytest

from jsonstarpc.functions import Function
from jsonstarpc.exceptions import InvalidRequest, ParseError, MethodNotFound
from jsonstarpc.utils import parse_json, validate_request, get_function


class TestParseJson:

    def test_one(self):
        with pytest.raises(ParseError):
            json_missing_bracket = """
            {
                "key": "value"
            
            """
            parse_json(json_missing_bracket)

    def test_two(self):
        with pytest.raises(ParseError):
            json_missing_double_quotes = """
            {
                key: "value"
            }
            """
            parse_json(json_missing_double_quotes)


class TestFindMethod:

    def test_method_not_found_one(self):
        def add(x, y):
            return x + y

        def sub(x, y):
            return x - y

        add_func = Function(add)
        sub_func = Function(sub)
        functions = [add_func, sub_func]

        with pytest.raises(MethodNotFound):
            get_function('addition', functions)

    def test_method_not_found_two(self):
        def add(x, y):
            return x + y

        def sub(x, y):
            return x - y

        add_func = Function(add, name='addition')
        sub_func = Function(sub, name='subtraction')
        functions = [add_func, sub_func]

        with pytest.raises(MethodNotFound):
            get_function('add', functions)

    def test_method_found_one(self):
        def add(x, y):
            return x + y

        def sub(x, y):
            return x - y

        add_func = Function(add)
        sub_func = Function(sub)
        functions = [add_func, sub_func]
        func = get_function('add', functions)
        assert func is add_func

    def test_method_found_two(self):
        def add(x, y):
            return x + y

        def sub(x, y):
            return x - y

        add_func = Function(add, name='addition')
        sub_func = Function(sub, name='subtraction')
        functions = [add_func, sub_func]
        func = get_function('addition', functions)
        assert func is add_func


class TestInvalidJsonRpcRequest:

    def test_not_a_dict(self):
        with pytest.raises(InvalidRequest):
            validate_request(True)

    def test_empty_dict(self):
        with pytest.raises(InvalidRequest):
            # empty dict
            request = {}
            validate_request(request)

    def test_missing_jsonrpc(self):
        with pytest.raises(InvalidRequest):
            # Missing 'jsonrpc'
            request = {"method": "add"}
            validate_request(request)

    def test_jsonrpc_invalid_type(self):
        with pytest.raises(InvalidRequest):
            # jsonrpc is not a string.
            request = {"jsonrpc": 2.0, "method": "add"}
            validate_request(request)

    def test_jsonrpc_invalid_value(self):
        with pytest.raises(InvalidRequest):
            # jsonrpc is not '2.0'
            request = {"jsonrpc": "3.0", "method": "add"}
            validate_request(request)

    def test_missing_method(self):
        with pytest.raises(InvalidRequest):
            # Missing 'method'
            request = {"jsonrpc": "2.0"}
            validate_request(request)

    def test_method_invalid_type(self):
        with pytest.raises(InvalidRequest):
            # 'method' is not a string.
            request = {"jsonrpc": "2.0", 'method': True}
            validate_request(request)

    def test_params_invalid_type(self):
        with pytest.raises(InvalidRequest):
            # 'params' is not a valid type.
            request = {"jsonrpc": "2.0", 'method': 'add', 'params': 1}
            validate_request(request)

    def test_id_invalid_type(self):
        with pytest.raises(InvalidRequest):
            # 'id' is not a valid type.
            request = {"jsonrpc": "2.0", 'method': 'add', 'id': None}
            validate_request(request)

    def test_valid_request_with_id(self):
        #  valid request
        request = {"jsonrpc": "2.0", 'method': 'add', 'params': [1, 2], 'id': 123}
        validate_request(request)

    def test_valid_request_without_id(self):
        #  valid request
        request = {"jsonrpc": "2.0", 'method': 'add', 'params': [1, 2]}
        validate_request(request)