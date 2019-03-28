import math
import random
from .base import BaseEffect
from dmx import JsonSerializeMixin

class FlickerDim(BaseEffect, JsonSerializeMixin):
    name = "Dim & Flicker"

    def __init__(self, device, length=None, seed=None):
        self.device = device
        self.length = length
        self.seed = seed
        self.counter = 0.0
        self.start_fade = 1.0
        self.finish_fade = 1.0
        self.dim_by = 0.5
        self._generator = random.Random(seed)

    def cancel(self, over_seconds=1.0):
        if self.length is not None and self.counter > self.length:
            raise Exception("This effect has already finished")
        self.length = self.counter + over_seconds
        self.finish_fade = over_seconds

    def update(self, dt):
        self.counter += dt

        if self.counter < self.start_fade:
            self._start_fade()
        elif self.length is not None and self.counter > self.length:
            self._finish_fade()
        else:
            self._main()

        if self.length is None or self.counter > self.length + self.finish_fade:
            return None
        return [self]

    def _start_fade(self):
        dim_amp = 1 - (self.dim_by * (self.counter / self.start_fade))
        self.device.Red.value = self.device.Red.value * dim_amp
        self.device.Green.value = self.device.Green.value * dim_amp
        self.device.Blue.value = self.device.Blue.value * dim_amp
        self.device.Amber.value = self.device.Amber.value * dim_amp

    def _main(self):
        rand = self._generator.random()
        dim_amp = min(1 - self.dim_by, rand)
        self.device.Red.value = self.device.Red.value * dim_amp
        self.device.Green.value = self.device.Green.value * dim_amp
        self.device.Blue.value = self.device.Blue.value * dim_amp
        self.device.Amber.value = self.device.Amber.value * dim_amp

    def _finish_fade(self):
        dim_amp = 1 - (self.dim_by * (1 - ((self.counter - self.length) / self.finish_fade)))
        self.device.Red.value = self.device.Red.value * dim_amp
        self.device.Green.value = self.device.Green.value * dim_amp
        self.device.Blue.value = self.device.Blue.value * dim_amp
        self.device.Amber.value = self.device.Amber.value * dim_amp