from aiohttp import web
import json
import weakref


# TODO: Serialisable mixin
# TODO: __json__/__xml__ with parent & depth parameters

class RecursiveEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return super().default(obj)


class RestAPI:
    def __init__(self, stage, host="localhost", port=8080):
        self.stage = stage
        self.host = host
        self.port = port

    async def _get_universes(self, request):
        return web.Response(text=json.dumps(self.stage.u, cls=RecursiveEncoder), headers={"Content-Type": "application/json"})

    def _register_routes(self, app):
        app.add_routes([web.get('/universes', self._get_universes)])

    async def start(self):
        app = web.Application()
        self._register_routes(app)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
