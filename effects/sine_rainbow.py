import math
from .base import BaseEffect
from dmx import JsonSerializeMixin

class SineRainbow(BaseEffect, JsonSerializeMixin):
    name = "Sin Colour Rainbow"

    def __init__(self, devices, speed=1.0, offset=0):
        self.devices = devices if hasattr(devices, '__iter__') else [devices]
        self.counter = offset
        self.speed = speed
        self.offset = offset

    def update(self, dt):
        self.counter += dt

        for dev in self.devices:
            dev.Red.value = max(0, math.sin((self.counter + 0) * self.speed) * 511 - 256)
            dev.Green.value = max(0, math.sin((self.counter + math.pi/2) * self.speed) * 511 - 256)
            dev.Blue.value = max(0, math.sin((self.counter + math.pi) * self.speed) * 511 - 256)
            dev.Amber.value = max(0, math.sin((self.counter + 3*math.pi/2) * self.speed) * 511 - 256)

        return [self]