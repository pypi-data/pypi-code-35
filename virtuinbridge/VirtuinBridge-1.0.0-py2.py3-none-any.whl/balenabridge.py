"""BalenaBridge shall be used to launch remote Balena device tests from Anduin."""
from __future__ import print_function
import time
from anduinrestserver import AnduinRestServer
from helper import getAnduinGlobalStubs, getAnduinGlobalData


class BalenaBridge(object):
    """ Launch Balena device tests from Anduin via IronPython script """
    def __init__(self, anduinGlobals, anduinDBPort=8008):
        self.anduinGlobals = getAnduinGlobalStubs()
        self.anduinGlobals.update(anduinGlobals or {})
        self.anduinDBPort = anduinDBPort
        self.anduinAPIProxy = AnduinRestServer(self.anduinGlobals, self.anduinDBPort)

    def getAnduinData(self):
        return getAnduinGlobalData(self.anduinGlobals)

    def runAPIProxy(self):
        try:
            self.anduinAPIProxy.start()
            while self.anduinAPIProxy.is_alive():
                time.sleep(2)
            self.anduinAPIProxy.shutdown()
        except KeyboardInterrupt:
            self.anduinAPIProxy.shutdown()
        except Exception:  # pylint: disable=broad-except
            self.anduinAPIProxy.shutdown()
        finally:
            self.anduinAPIProxy.join()

    def runTest(self, test, address='localhost'):
        """
        Runs test given supplied test configs.
        Args:
            test (dict): Test definition
        Returns:
            str|None: Error message or None
            list: Results list of dict objects
        """
        try:
            # Start Anduin API Proxy
            self.anduinAPIProxy.start()
            self.anduinAPIProxy.startTest(test, address=address)
            startTimeout = 30
            while self.anduinAPIProxy.is_alive() and startTimeout > 1:
                time.sleep(1)
                if self.anduinAPIProxy.testStatus['state'] in ['IDLE', 'START_REQUEST']:
                    startTimeout -= 0.5
                if self.anduinAPIProxy.testStatus['state'] in ['FINISHED', 'KILLED']:
                    self.anduinAPIProxy.shutdown()
                    self.anduinAPIProxy.join()
            return self.anduinAPIProxy.testStatus

        # Catch any exceptions
        except KeyboardInterrupt:
            self.anduinAPIProxy.stopTest(test, address=address)
            self.anduinAPIProxy.shutdown()
            self.anduinAPIProxy.join()
            status = self.anduinAPIProxy.testStatus
            status['error'] = 'Process terminated by user'
            return status
        except Exception as err:  # pylint: disable=broad-except
            self.anduinAPIProxy.stopTest(test, address=address)
            self.anduinAPIProxy.shutdown()
            self.anduinAPIProxy.join()
            status = self.anduinAPIProxy.testStatus
            status['error'] = err.message
            return status


if __name__ == "__main__":
    try:
        bridge = BalenaBridge(dict(), 8008)
        bridge.runAPIProxy()
    except Exception as err:  # pylint: disable=broad-except
        print('Following exception occurred: ', err)
