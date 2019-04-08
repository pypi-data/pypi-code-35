import asyncio
import unittest
from typing import Union

from image_processor_client import Client


class ImageClientTest(unittest.TestCase):

    RIP_MEME_TEXT = "Test Test Test"
    RIP_MEME_AVATAR_URL = "https://cdn.discordapp.com/avatars/331793750273687553/a_c59ddca1e44a4acb72654999459c58e0.gif"

    @staticmethod
    def __run_async(function):
        return asyncio.get_event_loop().run_until_complete(function)

    def test_client(self):
        client = Client()
        self.__run_async(client.close())
        self.assertIsInstance(client, Client)

    def test_client_with_loop(self):
        loop = asyncio.get_event_loop()
        client = Client(loop=loop)
        self.__run_async(client.close())
        self.assertIsInstance(client, Client)

    def test_get_rip_meme(self):
        return self.__run_async(self._get_rip_meme())

    async def _get_rip_meme(self):
        client = Client()
        meme_bytes = await client.memes.rip(self.RIP_MEME_TEXT, self.RIP_MEME_AVATAR_URL)
        self.assertIsInstance(meme_bytes, Union[bytes])
