from abc import ABC

from .models import ImageFunction


class MemeFunctions(ImageFunction, ABC):

    async def rip_meme(self, text: str, avatar_url: str):
        payload = {
            "text": text,
            "avatar_url": avatar_url
        }
        route = self.route("/memes/rip/")
        data = await self.request(route, json=payload)
        return data
