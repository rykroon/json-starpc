import inspect

from starlette.applications import Starlette
from starlette.responses import JSONResponse



async def send_code():
    ...

async def verify_code():
    ...


procedures = {
    'send_code': send_code,
    'verify_code': verify_code
}



async def homepage(request):
    data = await request.json()
    assert data['jsonrpc'] == "2.0"

    method = data['method']
    params = data.get('params', [])

    proc = procedures[method]
    sig = inspect.signature(proc)
    try:
        ba = sig.bind(*params) if isinstance(params, list) else sig.bind(**params)
    except TypeError:
        ...

    result = proc(*ba.args, **ba.kwargs)

    


app = Starlette()