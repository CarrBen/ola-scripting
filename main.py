from dmx import Universe, RGBAPar
from ola import OLAInterface
import asyncio
import time
#from aiohttp import web

from effects.sine_rainbow import SineRainbow
from effects.constant_colour import ConstantColour
from stages import studio
from control import RestAPI

# TODO: Logging
# TODO: Make HTTP API do stuff
# TODO: Loop signal handlers/graceful shutdown
# TODO: Debug tool
# TODO: Make it more library like
# TODO: Background/Transient Effects
# TODO: str/repr for Effects
# TODO: Docstrings/typehints
# TODO: More generic than just DMX?

class EffectScheduler:
    def __init__(self, interval, update_cb):
        self.interval = interval
        self.update_cb = update_cb
        self.last_run = None
        self.time_bank = 0
        self._tasks = []

    async def start(self):
        self.loop = asyncio.get_event_loop()
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
            self._run_tasks(self.interval)
            self.time_bank -= self.interval

        await self.update_cb()

    async def _run_tasks(self, dt):
        new_tasks = []

        for task in self._tasks:
            next_tasks = task.update(dt)

            if next_tasks is None:
                continue

            for nt in next_tasks:
                new_tasks.append(nt)

        self._tasks = new_tasks

    def add_task(self, task):
        self._tasks.append(task)

    async def kill(self, universe):
        universe.kill()
        await self.update_cb()


interface = OLAInterface(studio.u, "http://localhost:9090/set_dmx")
effect_scheduler = EffectScheduler(1.0/25, interface.send_update)
for dev in studio.u.devices:
    #scheduler.add_task(ConstantColour(dev, colour=(0, 0, 0, 50)))
    effect_scheduler.add_task(SineRainbow(dev))
rest_api = RestAPI(studio)

loop = asyncio.get_event_loop()
tasks = asyncio.gather(effect_scheduler.start(), rest_api.start())
try:
    loop.run_until_complete(tasks)
except KeyboardInterrupt:
    pass

#studio.u.kill()
loop.run_until_complete(effect_scheduler.kill(studio.u))
#interface.send_update_sync()
