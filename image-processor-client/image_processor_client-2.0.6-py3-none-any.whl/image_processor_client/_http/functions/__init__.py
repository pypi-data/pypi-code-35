from abc import ABC

from .memes import MemeFunctions
from .discord import DiscordFunctions


FUNCTIONS = [
    MemeFunctions,
    DiscordFunctions
]


class ImageFunctions(*FUNCTIONS, ABC):

    pass
