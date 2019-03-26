"""VirtuinBridge shall be used to launch Virtuin-based tests from Anduin."""
from __future__ import print_function
import json
import tempfile
import os
import time
from anduinxmlserver import AnduinXMLServer
from helper import runCommand
from helper import getAnduinGlobalStubs, getAnduinGlobalData, getVirtuinPath
try:  # Python 3 modules
    from urllib.request import urlopen
except ImportError:  # Python 2 modules
    from urllib2 import urlopen


class VirtuinBridge(object):
    """ Launch Virtuin from Anduin via IronPython script. """
    def __init__(self, anduinGlobals, anduinDBPort=8008):
        self.anduinGlobals = getAnduinGlobalStubs()
        self.anduinGlobals.update(anduinGlobals or {})
        self.anduinDBPort = anduinDBPort
        self.anduinAPIProxy = AnduinXMLServer(self.anduinGlobals, self.anduinDBPort)

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

    def runCollection(self, collection, resultDBURL=None):
        """
        Runs Virtuin based test given supplied configs.
        Returns all results returned by test.
        Args:
            collection (dict): Virtuin Collection
        Returns:
            str|None: Error message or None
            list: Results list of dict objects
        """
        errcode = 2
        error = None
        try:
            print('[VIRT] START COLLECTION')
            # Create I/O files for Virtuin
            collectionPath = tempfile.mktemp(dir=None, suffix='.json')
            print('[VIRT] Collection path: {0}'.format(collectionPath))
            errcode = 0
            # pylint: disable=unused-variable
            stdout = ''
            stderr = ''
            # Write test configs to file
            with open(collectionPath, 'w') as fp:
                json.dump(collection, fp, skipkeys=True, ensure_ascii=True)

            # Start Anduin API Proxy
            print('[VIRT] anduinAPIProxy.start()')
            self.anduinAPIProxy.start()
            print('[VIRT] anduinAPIProxy.startTest()')
            self.anduinAPIProxy.startTest()
            # Run Virtuin and block until complete
            print('[VIRT] anduinAPIProxy.getVirtuinPath()')
            virtuinGUI = getVirtuinPath()
            cmd = [virtuinGUI, '--collection', collectionPath]
            # This blocks until process exits
            print('[VIRT] bridge.runCommand()')
            stdout, stderr, errcode = runCommand(args=cmd, inputStr=None)
            error = stderr
            print('[VIRT] anduinAPIProxy.shutdown()')
            self.anduinAPIProxy.shutdown()
            self.anduinAPIProxy.join()
            # 0 = FINISHED and PASSED, 1 = FINISHED and FAILED...
            if errcode == 0 or errcode == 1:
                if resultDBURL:
                    results = json.loads(urlopen(resultDBURL).read())
                    error = self.anduinAPIProxy.processTestResults(results.get('results', []))
            os.remove(collectionPath)
            print('[VIRT] DONE COLLECTION')
            return errcode, error

        # Catch any exceptions
        except KeyboardInterrupt:
            self.anduinAPIProxy.shutdown()
            self.anduinAPIProxy.join()
            error = 'Process terminated by user'
            return errcode, error

        except Exception as err:  # pylint: disable=broad-except
            print('virtuinbridge.Exception', err)
            self.anduinAPIProxy.shutdown()
            self.anduinAPIProxy.join()
            error = err.message
            return errcode, error


if __name__ == "__main__":
    try:
        bridge = VirtuinBridge(dict(), 8008)
        bridge.runAPIProxy()
    except Exception as err:  # pylint: disable=broad-except
        print('Following exception occurred: ', err)
