# -*- coding: utf-8 -*-
"""TODO: making new library , totally outdated testlink"""


from qacode.core.exceptions.core_exception import CoreException
# TODO: import qatestlink


class ReporterTestlink(object):
    """Testlink API manager class"""

    # Testlink connection
    conn = None
    # Testlink Proyects list
    proyects = None
    # Testlink TestPlans list by proyect id
    plans = None
    # Testlink Builds list by testplan id
    builds = None

    def __init__(self,
                 logger_manager=None,
                 url_api=None,
                 dev_key=None):
        """Instance testlink api and save as self.conn property

        Keyword Arguments:
            logger_manager {[qacode.core.loggers.LoggerManager]} -- Class used
                for logging, raise if None obtained (default: None)
            url_api {[str]} -- url to TestlinkAPI (default: None)
            dev_key {[str]} -- developerKey for TestlinkAPI (default: None)

        Raises:
            CoreException -- If LoggerManager it's None
        """
        if logger_manager is None:
            raise CoreException(msg='Testlink logger_manager can\'t be None')
        self.logger_manager = logger_manager
        # connect with success params
        self.conn = self.connect()
        # verify content exist
        self.load()

    def connect(self, url_api=None, dev_key=None):
        """Connect to testlink XMLRPC"""
        raise NotImplementedError('Open an issue on Github')

    def load(self):
        """Load all TestProyects, TestPlans, Builds, Testsuites y TestCases"""
        raise NotImplementedError('Open an issue on Github')
