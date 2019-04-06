import sys
import click


"""
Harmonator

Download Harmontown podcasts

Format: Harmontown - S01E01 - 2019-01-01.mp4
"""

__author__ = "Chris Read"
__email__ = "centurix@gmail.com"

EXIT_OK = 0
EXIT_HELP = 2
HARMONTOWN_URL = "http://download.harmontown.com/video"


@click.command()
@click.option("--episode", default=None, help="Episode number to download")
@click.argument("destination", default=".")
def download(episode, destination):
    """
    With no specific episode
    1. Scan the destination folder looking for existing HT episodes
    2. Return the latest
    3. Scan the download URL for newer ones
    4. Download the newest one
    5. Rename

    With a specific episode
    1. Find URL's from the first known episode and count forward
    2. Once the episode is found, download it
    3. Rename

    With a date
    1. Find URL's from the specific date and count forward
    2. Once the episode is found, download it
    3. Rename

    :param episode:
    :param destination:
    :return:
    """
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(download())  # pragma: no cover
