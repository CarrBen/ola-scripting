import aiohttp


class OLAInterface:
    def __init__(self, url):
        self.url = url
        self.session = aiohttp.ClientSession()

    async def update(self, universe):
        async with self.session.post(url, data=self._serialise(universe)) as response:
            return response.status == 200

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
