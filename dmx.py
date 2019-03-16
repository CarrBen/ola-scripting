
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
        return (c for dev in self._devices for c in dev.channels)

    @property
    def devices(self):
        return self._devices

    def kill(self):
        for dev in self._devices:
            dev.kill()


class Device:
    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.universe = None

        self._channels = []
        for attr, channel in vars(self.__class__).items():
            if not self._filter_channel(channel):
                continue
            new_channel = channel.init(self.id, self)
            setattr(self, attr, new_channel)
            self._channels.append(new_channel)

    def __str__(self, specific=None):
        if specific is None:
            return f'<{self.__class__.__name__} {self.id} "{self.name}">'
        return f'<{self.__class__.__name__} {self.id} "{self.name}" {specific}>'

    @property
    def channels(self):
        return self._channels

    def _filter_channel(self, var):
        return issubclass(type(var), (Channel, OffsetChannel))

    def _resolve_channel(self, channel):
        return channel.init(self.id)

    def kill(self):
        for chan in self._channels:
            chan.kill()

DARK = "DARK"

class Channel:
    def __init__(self, id, name, value=0, on_kill=DARK):
        self.id = id
        self.name = name
        self._value = value
        self.device = None
        self.on_kill = on_kill

    def __str__(self):
        return f'<{self.__class__.__name__} {self.id} "{self.name}">'

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if v > 255 or v < 0:
            raise ValueError(f"Value for {self} of {self.device} must be between 0 and 255 inclusive. Was {v}.")
        self._value = v

    def init(self, base_channel, device):
        self.device = device
        return self

    def kill(self):
        if self.on_kill == DARK:
            self._value=0


class OffsetChannel:
    def __init__(self, offset, name, value=0, on_kill=DARK):
        if offset < 0 or offset > 512:
            raise ValueError(f"Value {offset} for offset is invalid. Must be between 0 and 512.")
        self._offset = offset
        self._kwargs = {
            'name': name,
            'value': value,
            'on_kill': on_kill
        }

    def __repr__(self):
        return f"{self.__class__.__name__}(offset={self._offset}, name=\"{self._kwargs['name']}\", value={self._kwargs['value']})"

    def __str__(self):
        return f'<{self.__class__.__name__} {self._offset:+} "{self._kwargs["name"]}">'

    def init(self, base_channel, device):
        chan = Channel(base_channel + self._offset, **self._kwargs)
        chan.device = device
        return chan


class RGBAPar(Device):
    Red = OffsetChannel(0, "Red")
    Green = OffsetChannel(1, "Green")
    Blue = OffsetChannel(2, "Blue")
    Amber = OffsetChannel(3, "Amber")

    def __str__(self):
        extra = " ".join(map(lambda c: str(c), self._channels))
        return super().__str__(extra)
