from dmx import Universe, RGBAPar
from ola import OLAInterface
import asyncio
import time

from effects.sine_rainbow import SineRainbow
from effects.constant_colour import ConstantColour
from stages import studio


class LightScheduler:
    def __init__(self, interval, update_cb):
        self.interval = interval
        self.update_cb = update_cb
        self.last_run = None
        self.time_bank = 0
        self._tasks = []

    def start(self):
        return asyncio.run(self._start())

    async def _start(self):
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
    scheduler.add_task(ConstantColour(dev, colour=(0, 0, 0, 50)))

try:
    scheduler.start()
except:
    pass

studio.u.kill()
interface.send_update_sync()
