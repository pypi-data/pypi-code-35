import os
import threading
import time
import calendar
try:  # Python 3 modules
    from urllib.request import urlopen
    from xmlrpc.server import SimpleXMLRPCServer
    from xmlrpc.server import SimpleXMLRPCRequestHandler
except ImportError:  # Python 2 modules
    from urllib2 import urlopen
    from SimpleXMLRPCServer import SimpleXMLRPCServer
    from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler


class AnduinXMLServer(threading.Thread):
    """ Acts as Anduin DB proxy via XML-based RPC server. """
    def __init__(self, anduinGlobals, port):
        super(AnduinXMLServer, self).__init__()
        self.server = None
        self.anduinGlobals = anduinGlobals
        self.port = port
        self.testStatus = {
            "testName": None,
            "testUUID": None,
            "state": 'IDLE',
            "progress": 0,
            "passed": None,
            "error": None,
            "timestamp": 0
        }

    def startTest(self, test=None):
        try:
            self.updateStatus({
                "testName": "",
                "testUUID": None,
                "state": 'START_REQUEST',
                "progress": 0,
                "passed": None,
                "error": None
            })
        except Exception as err:
            self.updateStatus({
                "state": 'FINISHED',
                "passed": False,
                "error": "{0}".format(err)
            })

    def stopTest(self, test=None):
        try:
            self.updateStatus({
                "state": 'STOP_REQUEST',
                "passed": False,
                "error": "Test killed"
            })
            self.updateStatus({"state": 'KILLED', "passed": False})
        except Exception as err:
            self.updateStatus({
                "state": 'KILLED',
                "passed": False,
                "error": "{0}".format(err)
            })

    def getStatus(self, handler=None):
        return self.testStatus

    def updateStatus(self, status):
        self.testStatus.update(status)
        self.testStatus['timestamp'] = calendar.timegm(time.gmtime())

    def addResults(self, results):
        """
        XMLRPCServer routine to add DB results
        Args:
            results: Array of results
        Returns:
            bool: Success
        """
        self.processTestResults(results)
        return True

    def processTestResults(self, results):
        """
        Processes DB results
        Args:
            results: Array of results
        Returns:
            str: Error message
        """
        error = None
        results = results if isinstance(results, list) else [results]
        for result in results:
            try:
                self.processTestResult(result)
            except Exception as err:  # pylint: disable=broad-except
                error = err
        return error

    def processTestResult(self, result):
        """
        Processes DB result dict
        Args:
            result: DB result dict
        Returns:
            None
        """
        anduinGlobals = self.anduinGlobals
        rstType = result.get('type', '').lower()
        rstName = result.get('name', None)
        rstUnit = result.get('unit', None)
        rstValue = result.get('value', None)
        rstDisplay = result.get('display', False)
        if rstType == 'blob':
            value = rstValue.encode() if isinstance(rstValue, str) else rstValue
            anduinGlobals['AddResultBlob'](rstName, rstUnit, value)
        elif rstType == 'text':
            anduinGlobals['AddResultText'](rstName, rstUnit, rstValue, rstDisplay)
        elif rstType == 'scalar':
            anduinGlobals['AddResultScalar'](rstName, rstUnit, rstValue, rstDisplay)
        elif rstType == 'list':
            anduinGlobals['AddResultList'](rstName, rstUnit, rstValue)
        elif rstType == 'file':
            if str(type(rstValue)) == "<type 'unicode'>":
                anduinGlobals['AddResultText'](rstName, 'Link', '{0}'.format(rstValue))
            elif isinstance(rstValue, str):
                anduinGlobals['AddResultText'](rstName, 'Link', '{0}'.format(rstValue))
            elif isinstance(rstValue, dict):
                srcURL = rstValue.get('src')
                dstPath = rstValue.get('dst')
                dstFolder = os.path.dirname(dstPath)
                if not os.path.exists(dstFolder):
                    os.makedirs(dstFolder)
                with open(dstPath, 'wb') as fp:
                    fp.write(urlopen(srcURL).read())
                anduinGlobals['AddResultText'](rstName, 'Link', str.format('{:s}', dstPath))
            else:
                raise Exception('AddResultText: Value must be either string or dict.')
        elif rstType == 'flush':
            anduinGlobals['FlushMetrics']()
        elif rstType == 'channel':
            anduinGlobals['SetChannel'](rstValue)

    def run(self):
        """ Start proxy threaded """
        class RequestHandler(SimpleXMLRPCRequestHandler):
            """RequestHandler"""
            rpc_paths = ('/RPC', '/')
        self.server = SimpleXMLRPCServer(
            ("0.0.0.0", self.port),
            requestHandler=RequestHandler,
            allow_none=True
        )
        self.server.register_introspection_functions()
        self.server.register_function(self.addResults, 'addResults')
        self.server.register_function(self.updateStatus, 'updateStatus')
        self.server.serve_forever()

    def shutdown(self):
        """ Shutdown proxy"""
        if self.server:
            self.server.shutdown()
        self.server = None

if __name__ == '__main__':
    server = None
    try:
        server = AnduinXMLServer(anduinGlobals={}, port=8086)
        server.start()
        while server.is_alive():
            time.sleep(2)
        server.shutdown()
    except KeyboardInterrupt:
        server.shutdown()
    except Exception as err:  # pylint: disable=broad-except
        print(err)
        if server:
            server.shutdown()
    finally:
        if server:
            server.join()
