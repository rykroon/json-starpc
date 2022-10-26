
import pytest

from jsonstarpc.functions import Function
from jsonstarpc.exceptions import InvalidParams


async def no_params():
    ...

async def with_params(x, y, z):
    ...

async def positional_only_params(x, y, z, /):
    ...

async def keyword_only_params(*, x, y, z):
    ...



class TestNoParams:

    @pytest.mark.asyncio
    async def test_one(self):
        f = Function(no_params)
        with pytest.raises(InvalidParams):
            params = [1, 2]
            await f(params)

    @pytest.mark.asyncio
    async def test_two(self):
        f = Function(no_params)
        with pytest.raises(InvalidParams):
            params = {'a': 1}
            await f(params)

    @pytest.mark.asyncio
    async def test_three(self):
        f = Function(no_params)
        assert await f() is None


class TestFunctionWithParams:

    @pytest.mark.asyncio
    async def test_one(self):
        f = Function(with_params)
        with pytest.raises(InvalidParams):
            # wrong number of parameters
            await f()

    @pytest.mark.asyncio
    async def test_two(self):
        f = Function(with_params)
        with pytest.raises(InvalidParams):
            # wrong number of parameters.
            params = [1, 2]
            await f(params)

    @pytest.mark.asyncio
    async def test_three(self):
        f = Function(with_params)
        params = [1, 2, 3]
        assert await f(params) is None

    @pytest.mark.asyncio
    async def test_four(self):
        f = Function(with_params)
        with pytest.raises(InvalidParams):
            # incorrect named parameters.
            params = {'a': 1, 'b': 2, 'c': 3}
            await f(params)

    @pytest.mark.asyncio
    async def test_five(self):
        f = Function(with_params)
        params = {'x': 1, 'y': 2, 'z': 3}
        assert await f(params) is None


class TestPositionalOnlyParams:

    @pytest.mark.asyncio
    async def test_one(self):
        f = Function(positional_only_params)
        with pytest.raises(InvalidParams):
            # incorrect number of parameters.
            await f()

    @pytest.mark.asyncio
    async def test_two(self):
        f = Function(positional_only_params)
        with pytest.raises(InvalidParams):
            # incorrect number of parameters.
            params = [1, 2]
            await f(params)

    @pytest.mark.asyncio
    async def test_three(self):
        f = Function(positional_only_params)
        params = [1, 2, 3]
        assert await f(params) is None

    @pytest.mark.asyncio
    async def test_four(self):
        f = Function(positional_only_params)
        with pytest.raises(InvalidParams):
            # incorrect named parameters.
            params = {'a': 1, 'b': 2, 'c': 3}
            await f(params)

    @pytest.mark.asyncio
    async def test_five(self):
        f = Function(positional_only_params)
        with pytest.raises(InvalidParams):
            # Accepts positional arguments only.
            params = {'x': 1, 'y': 2, 'z': 3}
            await f(params)


class TestKeywordOnlyParams:

    @pytest.mark.asyncio
    async def test_one(self):
        f = Function(keyword_only_params)
        with pytest.raises(InvalidParams):
            # incorrect number of parameters.
            await f()

    @pytest.mark.asyncio
    async def test_two(self):
        f = Function(keyword_only_params)
        with pytest.raises(InvalidParams):
            # incorrect number of parameters.
            params = [1, 2]
            await f(params)

    @pytest.mark.asyncio
    async def test_three(self):
        f = Function(keyword_only_params)
        with pytest.raises(InvalidParams):
            # Accepts keyword only arguments.
            params = [1, 2, 3]
            await f(params)

    @pytest.mark.asyncio
    async def test_four(self):
        f = Function(keyword_only_params)
        with pytest.raises(InvalidParams):
            # incorrect named parameters.
            params = {'a': 1, 'b': 2, 'c': 3}
            await f(params)

    @pytest.mark.asyncio
    async def test_five(self):
        f = Function(keyword_only_params)
        params = {'x': 1, 'y': 2, 'z': 3}
        assert await f(params) is None
