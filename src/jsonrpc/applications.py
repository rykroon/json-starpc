from starlette.applications import Starlette



class JsonRpc:
    def __init__(self, methods=[], protocols=[]):
        self.methods = methods
        self.protocols = protocols

    async def __call__(self, scope, receive, send):
        scope['app'] = self
        assert scope['type'] in self.protocols
        
        # identify transport

        # parse json

        # find method

        # run method

        # return jsonrpc response

        
