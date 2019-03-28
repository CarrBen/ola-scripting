import aiohttp
import asyncio
import requests


# TODO: Auto setup of OLA with Universe & Device
class OLAInterface:
    def __init__(self, universe, url):
        self.universe = universe
        self.url = url
        self.session = None

    async def send_update(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=1))
        async with self.session.post(self.url, data=self._serialize(self.universe)) as resp:
            return resp.status == 200

    def send_update_sync(self):
        requests.post(self.url, data=self._serialize(self.universe))

    def _serialize(self, universe):
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
