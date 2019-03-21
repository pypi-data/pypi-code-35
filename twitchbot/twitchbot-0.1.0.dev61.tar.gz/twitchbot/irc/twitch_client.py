import logging
import aiohttp
import datetime

from .client import Client


class TwitchClient(Client):
    def __init__(self, nickname: str = None, token: str = None, channel: str = None, loop=None):
        self.log = logging.getLogger(__name__)

        super().__init__(nickname=nickname, token=token, channel=channel, loop=loop)

        self._is_mod = False
        self._send_counter_max = 20
        self._send_counter_max_mod = 100
        self._send_session_td = datetime.timedelta(seconds=30)
        self.session = aiohttp.ClientSession(loop=self._event_loop)

    async def connect(self, host: str = 'irc.chat.twitch.tv', port: int = 6667) -> None:
        return await super().connect(host, port)

    async def cap(self, capability: str) -> str:
        capability = 'twitch.tv/' + capability
        return await super().cap(capability)

    async def send_pmsg(self, message):
        await self.send(f'PRIVMSG #{self._channel} :{message}')

    async def send_session_check(self):
        if not self._send_session_dt or (self._send_session_dt + self._send_session_td < datetime.datetime.now()):
            await self.send_session_reset()

        if self._is_mod:
            return self._send_counter < self._send_counter_max_mod
        return self._send_counter < self._send_counter_max

    async def receive(self):
        response = await super().receive()

        if response.command:
            if response.command == 'USERSTATE':
                if response.tags:
                    if response.tags['display-name'].lower() == self._nickname:
                        mod = response.tags['mod']
                        if mod == '1':
                            mod = True
                        else:
                            mod = False
                        if not self._is_mod == mod:
                            self._is_mod = mod
                            self.log.debug(f'IRC moderator status set to {self._is_mod}')

        return response

    async def close(self):
        if self.session:
            await self.session.close()
        await super().close()
