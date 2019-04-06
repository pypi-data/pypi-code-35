from datetime import datetime
import re
from .exceptions.malformed_filename import MalformedFilename


def format_filename(episode, episode_date):
    return "Harmontown - S01E{} - {}.mp4".format(
        str(episode).zfill(3), episode_date.strftime("%Y-%m-%d")
    )


def parse_filename(episode_filename):
    if not episode_filename.startswith("Harmontown - S01E"):
        raise MalformedFilename()

    matches = re.match(
        r"Harmontown - S01E(\d+) - (\d+)-(\d+)-(\d+)\.mp4", episode_filename
    )

    return (
        int(matches.group(1)),
        datetime(
            int(matches.group(2)), int(matches.group(3)), int(matches.group(4))
        ),
    )
