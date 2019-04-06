"""Contains the core class for dsclient"""
from dsclient import utils


class GenericServer(object):
    """Generic Server class intended to be subclassed by DebugServer and DebugSession classes"""

    def __init__(self, host=None, port=None):
        """Initializes Server object

        Args:
            host (str, optional): hostname of existing Server to connect to (default="localhost")
            port (int): port number of existing Server to connect to
        """
        self._port = port
        self._hostname = host or "localhost"
        try:
            self._server_socket = utils.create_socket(self._port, host=self._hostname)
        except:
            raise Exception(
                "Could not connect to Server(%s,%s)" % (self._hostname, self._port)
            )

    def _send_req(self, command, **args):
        """Sends request to server socket.

        Request is constructed from name and **args

        Args:
            name (str): name of command
            **args (dict): key word args to place in 'args' dict

        Returns:
            'data' return value or None: returns the 'data' return value if exists or None

        Raises:
            Exception: raised when response received is an error
        """

        req = utils.create_request(command, **args)

        resp = utils.send(self._server_socket, req)

        if resp["status"] == "FAIL":
            raise Exception("Command %s failed: %s" % (command, resp["message"]))

        return resp["data"] if "data" in list(resp.keys()) else None


class DebugServer(GenericServer):
    """DebugServer Class for creating and communicating with DebugServer-js"""

    def __init__(self, host=None, port=None):
        """Initializes DebugServer object

        Args:
            host (str, optional): hostname of existing DebugServer to connect to (default="localhost")
            port (int): port number of existing DebugServer to connect to
        """
        self._port = port
        self._hostname = host or "localhost"
        self._sessions = dict()
        try:
            self._server_socket = utils.create_socket(self._port, host=self._hostname)
        except:
            raise Exception(
                "Could not connect to DebugServer(%s,%s)" % (self._hostname, self._port)
            )

        existing_sessions = self._send_req("getListOfSessions")
        for session in existing_sessions:
            self._sessions[session["name"]] = DebugSession(
                host=self._hostname, port=session["port"]
            )

    def set_config(self, ccxml_path):
        """Set ccxml file for DebugServer

        Args:
            ccxml_path (str): full path to ccxml file to set
        """
        return self._send_req("setConfig", path=ccxml_path)

    def get_config(self):
        """Get ccxml file in use by DebugServer

        Returns:
            str: ccxml file in use by DebugServer

        """
        return self._send_req("getConfig")

    def create_config(
        self, name, connection=None, device=None, board=None, directory=None
    ):
        """Creates a ccxml file using the provided parameters

        Args:
            name (str): name of ccxml file to create
            connection (str): connection name to use (required if board is ommitted)
            device (str): devicetype name to use (required if board is ommitted)
            board (str): board name to use (required if connection + device ommitted)
            directory (str): full path to directory location to place file

        """
        if board is None and (connection is None or device is None):
            raise Exception(
                "Need to provide either 'board' name or 'connection' and 'device' name"
            )

        args = dict()
        args["name"] = name
        if board is not None:
            args["board"] = board
        else:
            args["connection"] = connection
            args["device"] = device

        if directory is not None:
            args["directory"] = directory

        return self._send_req("createConfig", **args)

    def get_list_of_CPUs(self):
        """Returns list of CPU names

        Returns:
            list: list of CPU names
        """
        return self._send_req("getListOfCPUs")

    def get_list_of_devices(self):
        """Returns list of device names

        Returns:
            list: list of device names
        """
        return self._send_req("getListOfDevices")

    def get_list_of_connections(self):
        """Returns list of connection names

        Returns:
            list: list of connection names
        """
        return self._send_req("getListOfConnections")

    def get_list_of_configurations(self):
        """Returns list of configuration files

        Returns:
            list: list of configuration files
        """
        return self._send_req("getListOfConfigurations")

    def open_session(self, name):
        """Open a session for the provided session name

        Args:
            name (str): session name to open

        Returns:
            DebugSession: DebugSession object
        """
        if name in list(self._sessions.keys()):
            raise Exception("Session: %s is already open." % name)

        session_info = self._send_req("openSession", name=name)
        self._sessions[name] = DebugSession(
            host=self._hostname, port=session_info["port"]
        )

        return self._sessions[name]

    def terminate_session(self, name):
        """Terminates an open session

        Args:
            name (str): name of session to terminate

        Raises:
            Exception: raises exception if problem terminating session
        """
        if name not in list(self._sessions.keys()):
            raise Exception("DebugSession: %s not open." % name)
        self._sessions[name].stop()

        self._send_req("terminateSession", name=name)
        del self._sessions[name]

    def get_list_of_sessions(self):
        """Returns list of open sessions

        Returns:
            list: list of open sessions
        """
        return self._sessions

    def kill(self):
        """Kills Debug Server (including any open sessions) """
        for session_name in list(self._sessions.keys()):
            self.terminate_session(session_name)

        self._send_req("killServer")
        self._server_socket.close()


class DebugSession(GenericServer):
    """DebugSession class for controlling session"""

    def __init__(self, host=None, port=None):
        """
        Args:
            host (str, optional): hostname of DebugSession to connect to (default="localhost")
            port (int): port number of DebugSession to connect to

        Warning:
            You should never instantiate this class directly. Instead call the
            :py:meth:`DebugServer.open_session` function to create a DebugSession object
        """
        self._port = port
        self._hostname = host
        try:
            self._server_socket = utils.create_socket(self._port, host=self._hostname)
        except:
            raise Exception(
                "Could not connect to DebugSession(%s,%s)"
                % (self._hostname, self._port)
            )

    def connect(self):
        """Connect to the device."""
        self._send_req("connect")

    def disconnect(self):
        """Disconnect from the device."""
        self._send_req("disconnect")

    def erase(self):
        """Erases device's flash memory.

        """
        self._send_req("erase")

    def reset(self):
        """Resets device.

        """
        self._send_req("reset")

    def load(self, file, binary=False, address=None):
        """Loads image into device's flash.

        Args:
            file (str): full path to file to load into flash
            binary (boolean, optional): specify to load image as binary (default = False)
            address (int, optional): specify to load binary image at specifc address (only to be used when 'binary' is True; default=0x0)


        Raises:
            Exception if image fails to load
        """
        if address is None:
            address = 0x0

        self._send_req("load", file=file, binary=binary, address=address)

    def verify(self, file, binary=False, address=None):
        """Verifies image in device's flash.

        Args:
            file (str): full path to file to verify in flash
            binary (boolean, optional): specify to verify image as binary (default = False)
            address (int, optional): specify to verify binary image at specifc address (only to be used when 'binary' is True; default=0x0)


        Raises:
            Exception if image fails verification process
        """
        if address is None:
            address = 0x0

        self._send_req("verify", file=file, binary=binary, address=address)

    def evaluate(self, expression, file=None):
        """Evaluates an expression (after loading optional symbols file)

        Args:
            expression (str): C/GEL expression to evaluate
            file (str, optional): path to file containing symbols to load before evaluating

        Returns:
            int: result of evaluated expression


        Raises:
            Exception if expression is invalid.
        """
        result = None
        if file is not None:
            result = self._send_req("evaluate", expression=expression, file=file)
        else:
            result = self._send_req("evaluate", expression=expression)

        return result

    def read_data(self, address, page=0, num_bytes=1):
        """Read memory from device

        Args:
            address (int): address to read data from
            page (int, optional): page in memory to get address from (default = 0)
            num_bytes (int, optional): number of bytes to read

        Returns:
            list: list of bytes(ints) read


        Raises:
            Exception if address location is invalid.
        """
        return self._send_req(
            "readData", address=address, page=page, numBytes=num_bytes
        )

    def write_data(self, data, address, page=0):
        """Write to memory on device

        Args:
            data (list): list of bytes (ints) to write to memory
            address (int): address to read data from
            page (int, optional): page in memory to get address from (default = 0)


        Raises:
            Exception if address location is invalid.
        """
        return self._send_req("writeData", data=data, address=address, page=page)

    def read_register(self, name):
        """Read value from register

        Args:
            name (str): register name to read

        Returns:
            int: value of register read


        Raises:
            Exception if register name is invalid.
        """
        return self._send_req("readRegister", name=name)

    def write_register(self, name, value):
        """Write value to register on device

        Args:
            name (str): register name to write to
            value (int): value to write to register


        Raises:
            Exception if register name is invalid.
        """
        return self._send_req("writeRegister", name=name, value=value)

    def get_option(self, option_id):
        """Get the value of a device option

        Args:
            option_id (str): name of device option

        Returns:
            any: value of option


        Raises:
            Exception if option id is invalid.
        """
        return self._send_req("getOption", id=option_id)

    def set_option(self, option_id, value):
        """Set the value of a device option

        Args:
            option_id (str): name of device option
            value (any): value to set option to


        Raises:
            Exception if option id is invalid.
        """
        return self._send_req("setOption", id=option_id, value=value)

    def perform_operation(self, opcode):
        """Performs flash operation

        Args:
            opcode (str): name of operation to perform (opcode)

        Returns:
            any: returns value of performing operation


        Raises:
            Exception if opcode is invalid.
        """
        return self._send_req("performOperation", opcode=opcode)

    def run(self, asynchronous=False):
        """Issues the run command to the device

        Args:
            asynchronous (boolean, optional): run and return control immediately (default = False)
        """
        self._send_req("run", asynchronous=asynchronous)

    def halt(self, wait=False):
        """Halts the device

        Args:
            wait (boolean): wait until device is actually halted before returning
        """
        self._send_req("halt", wait=wait)

    def stop(self):
        """Stops the session thread but does not terminate the session."""
        self._send_req("stop")
        self._server_socket.close()
