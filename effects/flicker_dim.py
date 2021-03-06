import math
import random
from .base import BaseEffect
from dmx import JsonSerializeMixin

class FlickerDim(BaseEffect, JsonSerializeMixin):
    name = "Dim & Flicker"

    def __init__(self, devices, length=None, seed=None):
        self.devices = devices if hasattr(devices, '__iter__') else [devices]
        self.length = length
        self.seed = seed
        self.counter = 0.0
        self.start_fade = 1.0
        self.finish_fade = 1.0
        self.dim_by = 0.8
        self._generator = random.Random(seed)
        self._target = 1.0

    def cancel(self, over_seconds=1.0):
        if self.length is not None and self.counter > self.length:
            raise Exception("This effect has already finished")
        self.length = self.counter + over_seconds
        self.finish_fade = over_seconds

    def update(self, dt):
        self.counter += dt
        self._target += self._generator.randint(-1, 1) * 0.1
        self._target = max(0, min(1, self._target))

        self._main()

        if self.length is not None and self.counter > self.length + self.finish_fade:
            return None
        return [self]

    def _main(self):
        dim_amp = self.current_amplitude
        for dev in self.devices:
            dev.Red.value = dev.Red.value * dim_amp
            dev.Green.value = dev.Green.value * dim_amp
            dev.Blue.value = dev.Blue.value * dim_amp
            dev.Amber.value = dev.Amber.value * dim_amp

    @property
    def current_amplitude(self):
        dim = self.dim_by * self._target
        if self.counter < self.start_fade:
            return 1 - (dim * (self.counter / self.start_fade))
        elif self.length is not None and self.counter > self.length:
            return 1 - (dim * (1 - ((self.counter - self.length) / self.finish_fade)))

        return (1 - dim)