import asyncio
import logging

from jsonrpc.applications import JsonRpc
from jsonrpc.methods import Method


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.INFO)


async def add(x: int, y: int) -> int:
    await asyncio.sleep(2)
    logger.info("add")
    return x + y


methods = [
    Method(add)
]


app = JsonRpc(
    methods=methods
)
