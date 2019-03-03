import requests


class Universe:
    def __init__(self, id, name):
        self.name = name
        self.id = id
        self._devices = []

    def __str__(self):
        return f'<{self.__class__.__name__} {self.id} "{self.name}">'

    def add(self, device):
        if not issubclass(type(device), Device):
            raise f'{device} does not appear to be a Device'
        self._devices.append(device)

    @property
    def channels(self):
        return (c for dev in self._devices for  c in dev.channels)

    def serialise(self):
        chans = sorted(self.channels, key=lambda c: c.id)
        filled_chans = []
        for chan in chans:
            while chan.id - len(filled_chans) > 1:
                filled_chans.append('0')
            filled_chans.append(str(chan.value))

        return {
            'u': self.id,
            'd': ','.join(filled_chans)
        }


#class DeviceMeta:
#    def __new__(Meta, cls, bases, dict):
        

    
#class Device(metaclass=DeviceMeta):
class Device:
    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.universe = None
        self._channels = []

    def __str__(self):
        return f'<{self.__class__.__name__} {self.id} "{self.name}">'

    @property
    def channels(self):
        return self._channels


class Channel:
    def __init__(self, id, name, value=0):
        self.id = id
        self.name = name
        self._value = value
        self.device = None

    def __str__(self):
        return f'<{self.__class__.__name__} {self.id} "{self.name}">'

    @property
    def value(self):
        return self._value


class RGBAPar(Device):
    Red = Channel(1, "Red")
    Green = Channel(2, "Green")
    Blue = Channel(3, "Blue")
    Amber = Channel(4, "Amber")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._channels = [self.Red, self.Green, self.Blue, self.Amber]


def update_uni(universe):
    data = universe.serialise()
    requests.post("http://localhost:9090/set_dmx", data=data)

u = Universe(1, "Test")
d = RGBAPar(1, "Test")
u.add(d)

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
        update_uni(u)
        time.sleep(0.01)
except KeyboardInterrupt:
    d.Red._value = 0
    d.Green._value = 0
    d.Blue._value = 0
    d.Amber._value = 0
    update_uni(u)
