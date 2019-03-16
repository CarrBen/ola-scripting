import aiohttp
import asyncio


class OLAInterface:
    def __init__(self, universe, url):
        self.universe = universe
        self.url = url
        self.session = None

    async def send_update(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        #print(self._serialise(self.universe)['d'])
        async with self.session.post(self.url, data=self._serialise(self.universe)) as resp:
            return resp.status == 200

    def _serialise(self, universe):
        chans = sorted(universe.channels, key=lambda c: c.id)
        filled_chans = []
        for chan in chans:
            while chan.id - len(filled_chans) > 1:
                filled_chans.append('0')
            filled_chans.append(str(chan.value))

        return {
            'u': universe.id,
            'd': ','.join(filled_chans)
        }
