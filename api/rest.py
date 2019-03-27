from aiohttp import web
import json
import weakref

from effects import FlickerDim
from effects.base import EffectMeta, BaseEffect


# TODO: Serialisable mixin
# TODO: __xml__ with parent & depth parameters?
# TODO: More specific serialisation?

class RecursiveEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return super().default(obj)


class RestAPI:
    def __init__(self, stage, effects, host="localhost", port=8080):
        self.stage = stage
        self.effects = effects
        self.host = host
        self.port = port

    async def _get_universes(self, request):
        return web.Response(text=json.dumps(self.stage.u, cls=RecursiveEncoder), headers={"Content-Type": "application/json"})

    async def _get_effects(self, request):
        print(EffectMeta.effect_types)
        return web.Response(text="test")

    async def _get_tasks(self, request):
        return web.Response(text=json.dumps(self.effects._tasks, cls=RecursiveEncoder), headers={"Content-Type": "application/json"})

    async def task_test(self, request):
        self.effects.add_task(FlickerDim(self.stage.grid_front_right, length=10.0), 2)
        return web.Response(text="true")

    def _register_routes(self, app):
        app.add_routes([web.get('/universes', self._get_universes)])
        app.add_routes([web.get('/tasks', self._get_tasks)])
        app.add_routes([web.get('/effects', self._get_effects)])
        app.add_routes([web.get('/test_task', self.task_test)])

    async def start(self):
        app = web.Application()
        self._register_routes(app)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
