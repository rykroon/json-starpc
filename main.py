from jsonrpc.applications import JsonRpc
from jsonrpc.methods import Method


async def add(x: int, y: int) -> int:
    return x + y


methods = [
    Method(add)
]


app = JsonRpc(
    methods=methods
)
