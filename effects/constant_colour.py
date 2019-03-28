import math
from .base import BaseEffect
from dmx import JsonSerializeMixin

#TODO: Base effect class

class ConstantColour(BaseEffect, JsonSerializeMixin):
    NAME = "Constant Colour"

    def __init__(self, device, colour=(255, 255, 255, 255)):
        self.device = device
        self.colour = colour

    def update(self, dt):
        self.device.Red.value = self.colour[0]
        self.device.Green.value = self.colour[1]
        self.device.Blue.value = self.colour[2]
        self.device.Amber.value = self.colour[3]

        return [self]