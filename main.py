from dmx import Universe, RGBAPar
from ola import OLAInterface


interface = OLAInterface("http://localhost:9090/set_dmx")

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
        interface.update(u)
        time.sleep(0.01)
except KeyboardInterrupt:
    d.Red._value = 0
    d.Green._value = 0
    d.Blue._value = 0
    d.Amber._value = 0
    interface.update(u)
