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
        self.channels = List(map(self._resolve_channel, filter(self._filter_channel, vars(self.__class__))))

    def __str__(self, specific=None):
        if specific is None:
            return f'<{self.__class__.__name__} {self.id} "{self.name}">'
        return f'<{self.__class__.__name__} {self.id} "{self.name}" {specific}>'

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


class OffsetChannel:
    def __init__(self, offset, name, value=0):
        if offset < 0 or offset > 512:
            raise ValueError(f"Value {offset} for offset is invalid. Must be between 0 and 512.")
        self._offset = offset
        self._kwargs = {
            'name': name,
            'value': value
        }

    def __repr__(self):
        return f"{self.__class__.__name__}(offset={self._offset}, name=\"{self._kwargs['name']}\", value={self._kwargs['value']})"

    def __str__(self):
        return f'<{self.__class__.__name__} {self._offset:+} "{self._kwargs["name"]}">'

    def init(self, base_channel):
        return Channel(base_channel + self._offset, **kwargs) 


class RGBAPar(Device):
    Red = OffsetChannel(0, "Red")
    Green = OffsetChannel(1, "Green")
    Blue = OffsetChannel(2, "Blue")
    Amber = OffsetChannel(3, "Amber")

    def __str__(self):
        extra = " ".join(map(lambda c: str(c), self._channels))
        return super().__str__(extra)


def update_uni(universe):
    data = universe.serialise()
    requests.post("http://localhost:9090/set_dmx", data=data)

u = Universe(1, "Test")
d = RGBAPar(1, "Test")
print(d)
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
