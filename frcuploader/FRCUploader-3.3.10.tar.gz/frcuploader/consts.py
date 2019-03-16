#!/usr/bin/env python3
import pkg_resources

from .youtube import *

import tbapy

__version__ = pkg_resources.require("FRCUploader")[0].version

# Default Variables
DEBUG = False  # DON'T COMMIT THIS LINE IF TRUE
DEFAULT_TAGS = "{}, frcuploader, FIRST, omgrobots, FRC, FIRST Robotics Competition, robots, Robotics, {game}"
MATCH_TYPE = ("qm", "qf", "sf", "f1m")
DEFAULT_DESCRIPTION = """Footage of the {ename} is courtesy of {team}.

Red Alliance  ({red1}, {red2}, {red3}) - {redscore}
Blue Alliance ({blue3}, {blue2}, {blue1}) - {bluescore}

To view match schedules and results for this event, visit The Blue Alliance Event Page: https://www.thebluealliance.com/event/{ecode}

Follow us on Twitter (@{twit}) and Facebook ({fb}).

For more information and future event schedules, visit our website: {weblink}

Thanks for watching!"""

NO_TBA_DESCRIPTION = """Footage of the {ename} Event is courtesy of {team}.

Follow us on Twitter (@{twit}) and Facebook ({fb}).

For more information and future event schedules, visit our website: {weblink}

Thanks for watching!"""

CREDITS = """

Uploaded with FRC-YouTube-Uploader (https://github.com/NikhilNarayana/FRC-YouTube-Uploader) by Nikhil Narayana"""

VALID_PRIVACY_STATUSES = ("public", "unlisted", "private")

GAMES = {
    "2019": "FIRST Destination: Deep Space, Destination: Deep Space, Deep Space",
    "2018": "FIRST Power Up, FIRST POWER UP",
    "2017": "FIRST Steamworks, FIRST STEAMworks",
    "2016": "FIRST Stronghold",
    "2015": "Recycle Rush",
    "2014": "Aerial Assist",
    "2013": "Ultimate Ascent"
}

spreadsheetID = "18flsXvAcYvQximmeyG0-9lhYtb5jd_oRtKzIN7zQDqk"
rowRange = "Data!A1:G1"
firstrun = True
stop_thread = False
response = None
status = None
error = None
sleep_minutes = 600
retry = 0
retryforlimit = 0
retry_status_codes = get_retry_status_codes()
retry_exceptions = get_retry_exceptions()
max_retries = get_max_retries()
tags = None
mcode = None
youtube = get_youtube_service()
spreadsheet = get_spreadsheet_service()
tba = tbapy.TBA("wvIxtt5Qvbr2qJtqW7ZsZ4vNppolYy0zMNQduH8LdYA7v2o1myt8ZbEOHAwzRuqf")
sizes = ("bytes", "KB", "MB", "GB", "TB")
cerem = ("None", "Opening Ceremonies", "Alliance Selection", "Closing Ceremonies", "Highlight Reel")
queue_values = os.path.join(os.path.expanduser("~"), ".frc_queue_values.txt")
form_values = os.path.join(os.path.expanduser("~"), '.frc_form_values.json')
log_file = os.path.join(os.path.expanduser("~"), ".frc_log.txt")
rec_formats = (".ts", ".mkv", ".avi", ".mp4", ".flv", ".mov", ".flv")
