# -*- coding: utf-8 -*-

import logging.config

import re
from datetime import datetime, timezone

from buoy.base.device.device import Device
from buoy.base.device.threads.reader import DeviceReader
from buoy.base.service.daemon import Daemon
from buoy.base.utils.config import *
from buoy.base.database import DeviceDB
from acmplus.item import ACMPlusItem
from buoy.base.utils.argsparse import parse_args


logger = logging.getLogger(__name__)

DEVICE_NAME = "acmplus"
DAEMON_NAME = "acmplus"


class ACMPlusReader(DeviceReader):
    def __init__(self, **kwargs):
        super(ACMPlusReader, self).__init__(**kwargs)
        self.pattern = ("\s*(?P<vy>-?\d{1,}.\d{1,}),\s{1,}(?P<vx>-?\d{1,}.\d{1,}),\s{1,}(?P<time>\d{2}:\d{2}:\d{2})"
                        ",\s{1,}(?P<date>\d{2}-\d{2}-\d{4}),\s{1,}(?P<waterTemperature>-?\d{1,}.\d{1,}).*")

    def parser(self, data):
        result = re.match(self.pattern, data)
        if result:
            measurement = ACMPlusItem(
                date=datetime.now(tz=timezone.utc),
                vx=result.group("vx"),
                vy=result.group("vy"),
                water_temp=result.group("waterTemperature")
            )

            return measurement


class ACMPlus(Device):
    def __init__(self, *args, **kwargs):
        device_name = kwargs.pop('device_name', 'ACMPlus')
        super(ACMPlus, self).__init__(device_name=device_name, cls_reader=ACMPlusReader, *args, **kwargs)


class ACMPlusDaemon(ACMPlus, Daemon):
    def __init__(self, name, **kwargs):
        db_conf = kwargs.pop('database')
        service_conf = kwargs.pop('service')
        db = DeviceDB(db_config=db_conf, db_tablename=name, cls_item=ACMPlusItem)

        Daemon.__init__(self, daemon_name=DAEMON_NAME, daemon_config=service_conf)
        ACMPlus.__init__(self, db=db, **kwargs)

    def before_stop(self):
        self.disconnect()


def run(config_buoy: str, config_log_file: str):
    logging.config.dictConfig(load_config_logger(path_config=config_log_file))
    buoy_config = load_config(path_config=config_buoy)

    daemon = ACMPlusDaemon(name=DEVICE_NAME, **buoy_config)
    daemon.start()


def main():
    args = parse_args(path_config='/etc/buoy/acmplus')
    run(config_buoy=args.config_file, config_log_file=args.config_log_file)


if __name__ == "__main__":
    main()
