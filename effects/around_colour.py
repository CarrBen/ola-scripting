import math
from .base import BaseEffect
from dmx import JsonSerialiseMixin


class AroundColour(BaseEffect, JsonSerialiseMixin):
    NAME = "Fade Around Colour"

    def __init__(self, device, amplitudes=(15, 15, 15, 15)):
        self.device = device
        self.amplitudes = amplitudes
        self.counter = 0

    def update(self, dt):
        self.counter += dt
        self.device.Red.value = self.device.Red.value + self.amplitudes[0] * math.sin(self.counter)
        self.device.Green.value = self.device.Green.value + self.amplitudes[1] * math.sin(self.counter)
        self.device.Blue.value = self.device.Blue.value + self.amplitudes[2] * math.sin(self.counter)
        self.device.Amber.value = self.device.Amber.value + self.amplitudes[3] * math.sin(self.counter)

        return [self]