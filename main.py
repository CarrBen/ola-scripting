from dmx import Universe, RGBAPar
from ola import OLAInterface
import asyncio
import time
from aiohttp import web

from effects.sine_rainbow import SineRainbow
from effects.constant_colour import ConstantColour
from stages import studio

# TODO: Logging
# TODO: Make HTTP API do stuff
# TODO: Loop signal handlers/graceful shutdown
# TODO: Debug tool
# TODO: Make it more library like
# TODO: Background/Transient Effects
# TODO: str/repr for Effects
# TODO: Docstrings/typehints
# TODO: More generic than just DMX?

class LightScheduler:
    def __init__(self, interval, update_cb):
        self.interval = interval
        self.update_cb = update_cb
        self.last_run = None
        self.time_bank = 0
        self._tasks = []
        self.loop = None

    def start(self, additional_tasks=[]):
        self.loop = asyncio.get_event_loop()
        tasks = asyncio.gather(self._start(), self._api(), *additional_tasks)
        self.loop.run_until_complete(tasks)

    async def _get_tasks(self, request):
        return web.Response(text=str(self._tasks))

    async def _api(self):
        app = web.Application()
        app.add_routes([web.get('/', self._get_tasks)])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', 8080)
        await site.start()

    async def _start(self):
        self.last_run = self.loop.time()

        while True:
            self._schedule_call()
            await self._run()
            await asyncio.sleep(max(0, self.next_run - self.loop.time()))

    def _schedule_call(self):
        base = self.loop.time()
        diff = base - round(base)
        ticks = diff // self.interval
        self.next_run =  round(base) + (ticks + 1) * self.interval

    async def _run(self):
        self.time_bank += self.next_run - self.last_run
        self.last_run = self.next_run

        while self.time_bank >= self.interval:
            await self._run_tasks(self.interval)
            self.time_bank -= self.interval

        await self.update_cb()

    async def _run_tasks(self, dt):
        completed = []

        for task in self._tasks:
            if await task.update(dt):
                completed.append(task)

        for task in completed:
            self._tasks.remove(task)

    def add_task(self, task):
        self._tasks.append(task)


interface = OLAInterface(studio.u, "http://localhost:9090/set_dmx")
scheduler = LightScheduler(1.0/100, interface.send_update)
for dev in studio.u.devices:
    #scheduler.add_task(ConstantColour(dev, colour=(0, 0, 0, 50)))
    scheduler.add_task(SineRainbow(dev))

scheduler.start()

studio.u.kill()
interface.send_update_sync()
