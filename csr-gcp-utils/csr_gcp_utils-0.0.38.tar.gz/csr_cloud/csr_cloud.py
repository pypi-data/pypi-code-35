import logging
from logging.handlers import RotatingFileHandler, WatchedFileHandler
import os
import errno
from os.path import expanduser

class csr_cloud():
    def __init__(self, feature, input1=None, input2=None):
        self.cloudname = "gcp"
        self.feature = feature

        if self.feature == "HA":
            self.setup_logging(expanduser('~/cloud/' + self.feature), 'csr_ha.log')
            from .ha_gcp import csr_ha
            self.ha = csr_ha()

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

    def setup_logging(self, directory=None, logfile_name = None):
        try:
            if directory is None:
                directory = expanduser('~/' + self.feature + '/' + 'logs')

            path = directory + '/'
            self.mkdir_p(path)
            # logfile_name = self.feature + '_' + \
            #    str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H_%M_%S')) + '.log'
            if logfile_name is None:
                logfile_name = self.feature + '.log'

            if self.feature == "HA":
                hdlr = WatchedFileHandler(filename=os.path.join(directory, logfile_name), mode='a')

            else:
                hdlr = RotatingFileHandler(os.path.join(directory, logfile_name), mode='a', maxBytes=5 * 1024 * 1024,
                                           backupCount=2, encoding=None, delay=0)

            formatter = logging.Formatter(
                '%(module)15s:%(funcName)25s:%(lineno)4s %(asctime)s %(levelname)s %(message)s')
            hdlr.setFormatter(formatter)
            self.log = logging.getLogger(self.feature)
            if not len(self.log.handlers):
                self.log.addHandler(hdlr)
            self.log.setLevel(logging.INFO)
        except Exception as e:
            print("csr_cloud: setup_logging: exception {}. ".format(e))
            pass