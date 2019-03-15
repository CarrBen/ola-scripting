from dmx import Universe, RGBAPar
from ola import OLAInterface
import asyncio
import time


class Scheduler:
    def __init__(self, interval, update_cb, loop=None):
        self.interval = interval
        self.loop = loop or asyncio.get_event_loop()
        self.update_cb = update_cb
        self.last_run = None
        self.time_bank = 0

    def start(self):
        self.last_run = time.monotonic() / 1000.0
        self._schedule_call()
        self.loop.run_forever()

    def _schedule_call(self):
        base = time.monotonic()
        diff = base - round(base)
        ticks = diff // self.interval
        next =  round(base) + (ticks + 1) * self.interval
        self.loop.call_at(next, self._run)
        self.next_run = next

    def _run(self):
        print(self.last_run, self.next_run)
        self.time_bank += self.next_run - self.last_run
        self.last_run = self.next_run

        while self.time_bank >= self.interval:
            self._run_tasks()
            self.time_bank -= self.interval

        self.update_cb()
        self._schedule_call()

    def _run_tasks(self):
        pass


u = Universe(1, "Test")
d = RGBAPar(1, "Test")
u.add(d)

interface = OLAInterface("http://localhost:9090/set_dmx")
scheduler = Scheduler(1.0/25, lambda: interface.update(u))
scheduler.start()

import time
import math
i = 0
try:
    while True:
        i += 1
        d.Red._value = max(0, math.cos(i/10) * 255)
        #d.Green._value = max(0, math.cos((i+8)/10) * 255)
        d.Blue._value = max(0, math.cos((i+16)/10) * 255)
        #d.Amber._value = max(0, math.cos((i+24)/10) * 255)
        interface.update(u)
        time.sleep(0.01)
except KeyboardInterrupt:
    d.Red._value = 0
    d.Green._value = 0
    d.Blue._value = 0
    d.Amber._value = 0
    interface.update(u)
