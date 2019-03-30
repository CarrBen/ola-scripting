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
        v = TaskView(self.effects, self.stage)
        v.register(self.app)

    async def _get_universes(self, request):
        return json_response(json_serializers.serialize_default(self.stage.u))

    async def _get_effects(self, request):
        return json_response(json_serializers.serialize_default(list(EffectMeta.effect_types.values())))

    async def _get_tasks(self, request):
        return json_response(json_serializers.serialize_default(self.effects._tasks))

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


class TaskView:
    def __init__(self, scheduler, stage):
        self.scheduler = scheduler
        self.stage = stage

    def task_get_list(self):
        return jsonify(json_serializers.serialize_default(self.scheduler._tasks))

    def task_test(self):
        # task = FlickerDim(self.stage.grid_front_left, length=None)
        task = FlickerDim(self.stage.all, length=None)
        self.scheduler.add_task(task, 2)
        return jsonify(json_serializers.serialize_default(task))

    def register(self, app):
        app.add_url_rule('/tasks', view_func=self.task_get_list, methods=['GET'])
        app.add_url_rule('/tasks/test', view_func=self.task_test, methods=['GET'])
