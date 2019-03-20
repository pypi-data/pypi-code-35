from datetime import datetime

from soniclib import util
from soniclib import config

__metrics = dict()


def start(name):
    if name not in __metrics:
        __metrics[name] = dict()
    __metrics[name]["start"] = {"timestamp": datetime.now()}


def stop(name, status=0):
    __metrics[name]["stop"] = {"timestamp": datetime.now(), "status": status}


def clear():
    __metrics.clear()


def log():
    if not __metrics:  # nothing collected? just return.
        return

    util.message("Result:")

    total_start_timestamp = None
    total_stop_timestamp = datetime.now()
    total_status = 0

    for key, value in sorted(__metrics.items(), key=lambda p: p[1]["start"]["timestamp"]):
        if total_start_timestamp is None:
            total_start_timestamp = value["start"]["timestamp"]

        status = value["stop"]["status"] if "stop" in value else 1
        total_status += status

        stop_time = value["stop"]["timestamp"] if "stop" in value else datetime.now()
        total_stop_timestamp = stop_time

        duration = stop_time - value["start"]["timestamp"]
        util.message("%-10s - Duration: %s - Finished at: %s - %s" % (key, duration, stop_time.isoformat(), format_status(status)))

    if total_start_timestamp:
        util.message("%-10s - Duration: %s - Finished at: %s - %s" % ("TOTAL", total_stop_timestamp - total_start_timestamp, total_stop_timestamp.isoformat(), format_status(total_status)))


def format_status(status):
    if status > 0:
        return "FAILURE" if config.get(config.Keys.monochrome) else "\033[0;91mFAILURE\033[0;0m"
    else:
        return "SUCCESS" if config.get(config.Keys.monochrome) else "\033[0;92mSUCCESS\033[0;0m"
