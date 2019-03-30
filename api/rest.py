from aiohttp import web
import json
import weakref

from effects import FlickerDim
from effects.base import EffectMeta, BaseEffect

from . import json as json_serializers


from hypercorn.asyncio import serve
from hypercorn.config import Config as HyperConfig
from quart import Quart, Config
from quart.json import jsonify


class RestAPI:
    def __init__(self, stage, effects, host="127.0.0.1", port=8080):
        self.stage = stage
        self.effects = effects
        self.host = host
        self.port = port
        self.setup_app()

    def setup_app(self):
        self.app = Quart(__name__)
        v = UniverseView(self.stage.u)
        v.register(self.app)

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

    async def start(self, on_shutdown=None):
        config = HyperConfig.from_mapping({'bind': [f'{self.host}:{self.port}']})
        await serve(self.app, config)
        if on_shutdown is not None:
            on_shutdown()


class UniverseView:
    def __init__(self, universe):
        self.universe = universe

    def get_list(self):
        return jsonify(json_serializers.serialize_default([self.universe]))

    def get_by_id(self, id):
        print(id)
        return jsonify(json_serializers.serialize_default([self.universe]))

    def register(self, app):
        app.add_url_rule('/universes', view_func=self.get_list, methods=['GET'])
        app.add_url_rule('/universes/<int:id>', view_func=self.get_by_id, methods=['GET'])
