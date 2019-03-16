import math


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