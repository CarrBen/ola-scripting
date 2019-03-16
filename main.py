from dmx import Universe, RGBAPar
from ola import OLAInterface
import asyncio
import time
import math


class LightScheduler:
    def __init__(self, interval, update_cb):
        self.interval = interval
        self.update_cb = update_cb
        self.last_run = None
        self.time_bank = 0
        self._tasks = []

    def start(self):
        asyncio.run(self._start())

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


class SineRainbow:
    def __init__(self, device):
        self.device = device
        self.counter = 0
        self.speed = 1.0

    async def update(self, dt):
        self.counter += dt

        self.device.Red.value = max(0, math.sin((self.counter + 0) * self.speed) * 511 - 256)
        self.device.Green.value = max(0, math.sin((self.counter + math.pi/2) * self.speed) * 511 - 256)
        self.device.Blue.value = max(0, math.sin((self.counter + math.pi) * self.speed) * 511 - 256)
        self.device.Amber.value = max(0, math.sin((self.counter + 3*math.pi/2) * self.speed) * 511 - 256)

        return False


u = Universe(1, "Test")
d = RGBAPar(1, "Test")
u.add(d)

interface = OLAInterface(u, "http://localhost:9090/set_dmx")
scheduler = LightScheduler(1.0/25, interface.send_update)
scheduler.add_task(SineRainbow(d))
scheduler.start()


d.Red.value = 0
d.Green.value = 0
d.Blue.value = 0
d.Amber.value = 0
interface.send_update()
