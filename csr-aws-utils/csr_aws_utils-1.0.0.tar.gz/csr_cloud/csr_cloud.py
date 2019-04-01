import logging
from logging.handlers import RotatingFileHandler, WatchedFileHandler
import os
import errno
from as_aws import as_cloud
from ha_csr import HACsr

GUESTSHELL = "/home/guestshell/"
LOGS = "logs/"
CLOUD = "cloud/"
LOG = ".log"
FORSLASH = "/"
AWS = "aws"
AUTOSCALER = "autoscaler"
HA = "ha"
EVENTS = "events"


class csr_cloud():
    def __init__(self, feature, input1=None, input2=None):
        self.cloud_name = AWS

        self.feature = feature.lower()

        # Create the logger
        self.log = logging.getLogger(self.feature)

        if self.feature == AUTOSCALER:
            self.as_cloud = as_cloud()

        elif self.feature == HA:
            self.setup_logging()
            # Make event-log directory
            event_directory = GUESTSHELL + CLOUD  + FORSLASH + self.feature.upper() + FORSLASH + EVENTS
            self.mkdir_p(event_directory)
            self.ha = HACsr()

    def mkdir_p(self, path):
        try:
            os.makedirs(path, exist_ok=True)  # Python>3.2
        except TypeError:
            try:
                os.makedirs(path)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise

    def setup_logging(self):
        try:
            # Name the directory
            directory_name = GUESTSHELL + CLOUD  + FORSLASH + self.feature.upper()
            path = directory_name + FORSLASH
            # Create the directory
            self.mkdir_p(path)

            # Name the log file
            log_file = 'csr_ha.log'

            if self.feature == HA:
                handler = WatchedFileHandler(filename=os.path.join(directory_name, log_file), mode='a')

            else:

                # Create the file handler
                handler = RotatingFileHandler(os.path.join(directory_name, log_file), mode='a', maxBytes=5 * 1024 * 1024,
                                              backupCount=0, encoding=None, delay=0)

            # Create the format
            formatter = logging.Formatter(
                ' %(asctime)s  %(module)s:  %(funcName)s:%(lineno)s  %(levelname)s  %(message)s')

            # Set the format
            handler.setFormatter(formatter)

            # Add Handler
            if not len(self.log.handlers):
                self.log.addHandler(handler)

            # Set the log level
            self.log.setLevel(logging.DEBUG)

        except Exception as e:
            print("csr_cloud: setup_logging: exception {}. ".format(e))
            pass


if __name__ == '__main__':
    csr = csr_cloud('HA')