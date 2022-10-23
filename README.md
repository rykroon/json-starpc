# json-starpc
A JSON RPC Framework built using Starlette.


```
from starlette.application import Startlette
from jsonstarpc.functions import Function
from jsonstarpc.routing import JsonRpcRoute


async def add(x: int, y: int) -> int:
    return x + y


functions = [
    Function(add)
]

routes = [
    JsonRpcRoute('/', functions=functions)
]

app = Starlette(
  routes=routes
)
```
