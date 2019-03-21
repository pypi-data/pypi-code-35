from typing import Generator, Tuple

import twitch

from tcd.formats.custom import Custom
from tcd.formats.srt import SRT
from tcd.formats.ssa import SSA
from tcd.settings import Settings


class Formatter:

    def __init__(self, video: twitch.helix.Video):
        self.video: twitch.helix.Video = video

    def use(self, format_name: str) -> Tuple[Generator[Tuple[str, twitch.v5.Comment], None, None], str]:
        """
        Use format
        :param format_name:
        :return: tuple(Line, comment), output
        """
        if format_name not in Settings().config['formats']:
            print('Invalid format name')
            exit(1)

        if format_name == 'srt':
            return SRT(self.video).use()
        elif format_name == 'ssa':
            return SSA(self.video).use()
        else:
            return Custom(self.video, format_name).use()
