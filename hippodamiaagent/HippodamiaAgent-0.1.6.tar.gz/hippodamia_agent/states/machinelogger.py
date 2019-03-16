from tantamount.machine import Machine
from pelops.mylogger import get_child


class MachineLogger(Machine):
    logger = None
    def __init__(self, logger):
        Machine.__init__(self)
        self.logger = get_child(logger, self.__class__.__name__)

    def operate(self, eventid):
        self.logger.debug("operate - eventid: {}".format(eventid))
        try:
            Machine.operate(self, eventid)
        except KeyError as err:
            self.logger.info("operate - KeyError: {}".format(err))
        except Exception as e:
            self.logger.error("operate - Exception: {}".format(e))
            raise e

    def asyncoperate(self, eventid):
        self.logger.debug("asyncoperate - eventid: {}".format(eventid))
        Machine.asyncoperate(self, eventid)
