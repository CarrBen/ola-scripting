from aiohttp import web
import json
import weakref

from effects import FlickerDim
from effects.base import EffectMeta, BaseEffect

from . import json as json_serializers

# TODO: Serializable mixin
# TODO: __xml__ with parent & depth parameters?
# TODO: More specific serialization?

class RecursiveEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return super().default(obj)


def json_response(content, extra_headers={}, **kwargs):
    headers = {"Content-Type": "application/json"}
    headers.update(extra_headers)
    return web.Response(text=json.dumps(content), headers=headers, **kwargs)


class RestAPI:
    def __init__(self, stage, effects, host="localhost", port=8080):
        self.stage = stage
        self.effects = effects
        self.host = host
        self.port = port

    async def _get_universes(self, request):
        return json_response(json_serializers.serialize_default(self.stage.u))

    async def _get_effects(self, request):
        return json_response(json_serializers.serialize_default(list(EffectMeta.effect_types.values())))

    async def _get_tasks(self, request):
        return json_response(json_serializers.serialize_default(self.effects._tasks))

    async def task_test(self, request):
        task = FlickerDim(self.stage.grid_front_right, length=10.0)
        self.effects.add_task(task, 2)
        return web.Response(text=json.dumps(json_serializers.serialize_default(task)))

    def _register_routes(self, app):
        app.add_routes([web.get('/universes', self._get_universes)])
        app.add_routes([web.get('/tasks', self._get_tasks)])
        app.add_routes([web.get('/effects', self._get_effects)])

    async def start(self):
        app = web.Application()
        self._register_routes(app)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
