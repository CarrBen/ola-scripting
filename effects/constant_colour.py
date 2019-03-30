import math
from .base import BaseEffect
from dmx import JsonSerializeMixin

#TODO: Base effect class

class ConstantColour(BaseEffect, JsonSerializeMixin):
    name = "Constant Colour"

    def __init__(self, devices, colour=(255, 255, 255, 255)):
        self.devices = devices if hasattr(devices, '__iter__') else [devices]
        self.colour = colour

    def update(self, dt):
        for dev in self.devices:
            dev.Red.value = self.colour[0]
            dev.Green.value = self.colour[1]
            dev.Blue.value = self.colour[2]
            dev.Amber.value = self.colour[3]

        return [self]