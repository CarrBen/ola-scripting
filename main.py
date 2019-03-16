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


class SineRainbow:
    def __init__(self, device, speed=1.0, offset=0):
        self.device = device
        self.counter = offset
        self.speed = speed
        self.offset = offset

    async def update(self, dt):
        self.counter += dt

        self.device.Red.value = max(0, math.sin((self.counter + 0) * self.speed) * 511 - 256)
        self.device.Green.value = max(0, math.sin((self.counter + math.pi/2) * self.speed) * 511 - 256)
        self.device.Blue.value = max(0, math.sin((self.counter + math.pi) * self.speed) * 511 - 256)
        self.device.Amber.value = max(0, math.sin((self.counter + 3*math.pi/2) * self.speed) * 511 - 256)

        return False


u = Universe(1, "Test")
d = RGBAPar(161, "Test")
u.add(d)
d2 = RGBAPar(9, "Test2")
u.add(d2)
d3 = RGBAPar(81, "Test3")
u.add(d3)
d4 = RGBAPar(85, "Test4")
u.add(d4)
d5 = RGBAPar(33, "Test5")
u.add(d5)
d6 = RGBAPar(37, "Test3")
u.add(d6)
d7 = RGBAPar(49, "Test4")
u.add(d7)
d8 = RGBAPar(113, "Test5")
u.add(d8)
d9 = RGBAPar(1, "Test3")
u.add(d9)
d10 = RGBAPar(129, "Test4")
u.add(d10)
d11 = RGBAPar(65, "Test5")
u.add(d11)

interface = OLAInterface(u, "http://localhost:9090/set_dmx")
scheduler = LightScheduler(1.0/100, interface.send_update)
scheduler.add_task(SineRainbow(d, speed=5))
scheduler.add_task(SineRainbow(d2, offset=1, speed=5))
scheduler.add_task(SineRainbow(d3, offset=2, speed=5))
scheduler.add_task(SineRainbow(d4, offset=3, speed=5))
scheduler.add_task(SineRainbow(d5, offset=4, speed=5))
scheduler.add_task(SineRainbow(d6, offset=5, speed=5))
scheduler.add_task(SineRainbow(d7, offset=6, speed=5))
scheduler.add_task(SineRainbow(d8, offset=7, speed=5))
scheduler.add_task(SineRainbow(d9, offset=8, speed=5))
scheduler.add_task(SineRainbow(d10, offset=9, speed=5))
scheduler.add_task(SineRainbow(d11, offset=10, speed=5))

try:
    task = scheduler.start()
except:
    pass

u.kill()
interface.send_update_sync()
