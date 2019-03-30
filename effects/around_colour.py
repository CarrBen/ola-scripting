import math
from .base import BaseEffect
from dmx import JsonSerializeMixin


class AroundColour(BaseEffect, JsonSerializeMixin):
    name = "Fade Around Colour"

    def __init__(self, devices, amplitudes=(15, 15, 15, 15)):
        self.devices = devices if hasattr(devices, '__iter__') else [devices]
        self.amplitudes = amplitudes
        self.counter = 0

    def update(self, dt):
        self.counter += dt
        for dev in self.devices:
            dev.Red.value = dev.Red.value + self.amplitudes[0] * math.sin(self.counter)
            dev.Green.value = dev.Green.value + self.amplitudes[1] * math.sin(self.counter)
            dev.Blue.value = dev.Blue.value + self.amplitudes[2] * math.sin(self.counter)
            dev.Amber.value = dev.Amber.value + self.amplitudes[3] * math.sin(self.counter)

        return [self]