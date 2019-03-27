"""
Module to handle basic session
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import socket
import time

from ssh2.session import Session as Ssh2Session  # pylint: disable=E0611
from ssh2.utils import wait_socket  # pylint: disable=E0611
from ssh2.exceptions import AuthenticationError, SocketDisconnectError, SocketRecvError  # pylint: disable=E0611
from netssh2 import logger
from netssh2.exceptions import (
    NetSsh2Timeout,
    NetSsh2ChannelException,
    NetSsh2TooManyRetriesException,
    NetSsh2AuthenticationError,
    NetSsh2HostError
)
from netssh2.globals import LIBSSH2_ERROR_EAGAIN


class Session(object):  # pylint: disable=R0902
    """
    Defines default session to be used across multiple vendors.
    """

    def __init__(  # pylint: disable=R0913,R0914
            self,
            host="",
            user="",
            passwd="",
            port=22,
            timeout=5000,
            auth_retries=5,
            auth_delay=2000,
            socket_retries=100,
            socket_delay=100,
            prompt=None,  # TODO: Add automatic prompt detection
            command_prompt=None,
            newline="\n",  # TODO: Add automatic newline chars detection (can be \r\r\n for example)
            invoke_shell=False,
            verbose=True
    ):
        """

        :param host: host address to connect to
        :type host: string

        :param user: username for authentication
        :type user: string

        :param passwd: password for authentication
        :type passwd: string

        :param port: port number, default 22
        :type port: int

        :param timeout: timeout in miliseconds
        :type timeout: int

        :param auth_retries: number of retries for authentication
        :type auth_retries: int

        :param auth_delay: delay in miliseconds between authentication retries
        :type auth_delay: int

        :param socket_retries: number of retries for socket connection
        :type socket_retries: int

        :param socket_delay: delay in miliseconds between socket retries
        :type socket_delay: int

        :param prompt: commandline prompt to wait for with interactive shell
        :type prompt: string

        :param command_prompt: sometimes the prompt changes when command is issued, pass it here
        :type command_prompt: string

        :param newline: newline characters to confirm command, default \n
        :type newline: string

        :param invoke_shell: should we invoke interactive shell? default False
        :type invoke_shell: bool

        :param verbose: be verbose, print stuff from time to time, default True
        :type verbose: bool
        """
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port

        self.verbose = verbose

        # set timeout
        self.timeout = self._limit_timeout_value(int(timeout))

        self.auth_retries = auth_retries
        self.auth_delay = auth_delay
        self.socket_retries = socket_retries
        self.socket_delay = socket_delay
        self.prompt = prompt
        self.command_prompt = command_prompt or prompt
        self.newline = newline
        self.invoke_shell = invoke_shell

        self.sock = None
        self.session = None
        self.chan = None

        self.stdout = ""
        self.stdout_buff = ""
        self.stderr = ""
        self.stderr_buff = ""

        self.create_session()

        # With invoke shell we want to have channel open so we can run subsequent commands in the same shell
        if self.invoke_shell:
            self.open_channel()
            self.configure_channel()

    def set_prompt(self, new_prompt):
        """
        Setting different prompt with opened session.
        :param new_prompt: new string to wait for after command with invoke_shell
        :type new_prompt: string

        :return: True
        :rtype: bool
        """
        assert isinstance(new_prompt, type("")), "New prompt is not string."
        if self.prompt == self.command_prompt:
            self.command_prompt = new_prompt
        self.prompt = new_prompt
        return True

    @staticmethod
    def _limit_timeout_value(timeout):
        """
        This prevents from overflowing C long int
        :param timeout: timeout value
        :type timeout: int

        :return: timeout value that fits C long int
        :rtype: int
        """
        return timeout if timeout <= 2 ** 32 else 2 ** 32

    def _connect_socket(self, try_number=1):
        """
        This function is to handle socket errors and disconnections.
        When we get them, we need to start the whole socket operation again.
        logging.debug any socket exceptions.
        :param try_number:
        :type try_number:

        :raises:  netssh2.exceptions.NetSsh2TooManyRetriesException if socket_retries number is exceeded.
        :raises:  netssh2.exceptions.NetSsh2HostError when given invalid/unreachable host

        :return: True
        :rtype: bool
        """

        def _retry(_try_number):
            # Try again after some delay
            time.sleep(float(self.socket_delay) / 1000)
            return self._connect_socket(_try_number + 1)

        assert isinstance(self.socket_retries, int), "socket_retries is not int"
        assert isinstance(self.host, type("")), "host is not string"
        assert isinstance(self.port, int), "port is not it"
        assert isinstance(self.timeout, (float, int)), "timout is not either float or int"

        if try_number == self.socket_retries + 1:
            raise NetSsh2TooManyRetriesException("Could not establish socket connection after %s tries."
                                                 % self.socket_retries)
        try:
            # Create socket connection
            socket_connection = socket.create_connection((self.host, self.port), float(self.timeout) / 1000)
            # Create a session
            self.session = Ssh2Session()
            self.session.handshake(socket_connection)
        except SocketDisconnectError:
            logger().debug("Got SocketDisconnectError, trying to connect to socket again after delay. %s/%s",
                           try_number,
                           self.socket_retries)
            return _retry(try_number)
        except socket.gaierror:
            raise NetSsh2HostError("Name or service '%s' not known" % self.host)
        except socket.error as exception:
            logger().debug("Got socket.error: '%s', retrying connection to socket after delay. %s/%s", exception,
                           try_number, self.socket_retries)
            return _retry(try_number)

        return True

    def authenticate_session(self):
        """
        Tries to authenticate existing session

        :raises:  netssh2.exceptions.NetSsh2AuthenticationError when authentication fails
        :raises:  netssh2.exceptions.NetSsh2TooManyRetriesException if number of auth_retries is exceeded
        :raises:  netssh2.exceptions.Exception if any other issue happens when authenticating

        :return: True
        :rtype: bool
        """
        assert self.user, "user is not set"
        assert isinstance(self.user, type("")), "user is not string"
        assert self.passwd, "passwd is not set"
        assert isinstance(self.passwd, type("")), "passwd is not string"
        assert self.session, "session is not created"
        assert isinstance(self.auth_retries, int), "auth_restries is not int"

        i = 0
        while True:
            # Try to authenticate user
            try:
                self.session.userauth_password(self.user, self.passwd)
                break
            except AuthenticationError:
                raise NetSsh2AuthenticationError("Authentication failed when connecting to %s" % self.host)
            except (ValueError, OSError):
                logger().info("Could not SSH to %s, waiting for it to start", self.host)
                i += 1
            except SocketDisconnectError:
                logger().info("Socket got disconnected in between, connecting again.")
                self._connect_socket()
                i += 1
            except Exception as exception:
                logger().error("Could not SSH to %s", self.host)
                logger().debug("Exception: %s", exception)
                raise
            # If we could not connect within set number of tries
            if i == self.auth_retries:
                raise NetSsh2TooManyRetriesException("Could not connect to %s after %s retries. Giving up"
                                                     % (self.auth_retries, self.host))
            # Wait before next attempt
            time.sleep(float(self.auth_delay) / 1000)
        return True

    def create_session(self):
        """
        Connect to a host using ssh
        :return: True
        :rtype: bool
        """
        self._connect_socket()
        self.authenticate_session()
        self.configure_session()
        return True

    def disconnect(self):
        """
        Disconnect from a ssh session
        :return: True
        :rtype: bool
        """
        self.session.disconnect()

        # Clean up
        self.chan = None
        self.sock = None
        self.session = None
        return True

    def configure_session(self):
        """
        Sets up nonblocking mode, which allows to wait for socket to be ready and more control over channel.
        :return: True
        :rtype: bool
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session.set_blocking(False)

        assert isinstance(self.timeout, int), "timeout is not int"
        self.session.set_timeout(self.timeout)

        return True

    def open_channel(self):
        """
        Opens channel on ssh2 session.
        :raises:  netssh2.exceptions.NetSsh2ChannelException if the channel is not available for some reason.

        :return: True
        :rtype: bool
        """
        self.chan = self._execute_function(self.session.open_session)
        if not self.chan:
            raise NetSsh2ChannelException("Could not open channel.")
        return True

    def clean_shell_header(self):
        """
        Gets rid of interactive shell header.
        :raises:  netssh2.exceptions.NetSsh2Timeout in case of timeout when reading the channel.

        :return: True
        :rtype: bool
        """
        if self.prompt:
            self._clear_buffers()
            # Be sure to get prompt
            assert self.newline, "newline char is not set"
            self.chan.write(self.newline)  # TODO: Prompt detection here
            # wait for prompt
            assert isinstance(self.stdout_buff, type("")), "stdout_buff is not string"
            while self.prompt not in self.stdout_buff:
                try:
                    _, resp = self.read_chan(buff_size=9999)
                except NetSsh2Timeout:
                    logger().error("Waiting for prompt '%s' timed out after %s ms.", self.prompt, self.timeout)
                    resp = self.prompt
                self.stdout_buff += resp if isinstance(resp, type("")) else resp.decode('ascii', 'ignore')

        else:
            # get rid of the whole header
            self._execute_function(self.chan.read, size=65535)
        return True

    def configure_channel(self):
        """
        Does any channel configuration, for example invoking interactive shell if invoke_shell=True.
        :return: True
        :rtype: bool
        """
        if self.invoke_shell:
            # Make this interactive shell
            assert self.chan, "chan (channel) is not created/open"
            self._execute_function(self.chan.pty)
            self._execute_function(self.chan.shell)
            self.clean_shell_header()
        return True

    def read_chan(self, buff_size=1024, stderr=False):
        """
        Read channel output in non blocking way.
        :param buff_size: Buffer size to read from the channel
        :type buff_size: int

        :param stderr: Do we want to read STDERR (True) instead of STDOUT (False)?
        :type stderr: bool

        :raises:  netssh2.exceptions.NetSsh2Timeout in case of timeout when reading channel.

        :return: (size, buffer) size and payload read from the channel
        :rtype: tuple(int, str)
        """
        assert self.chan, "chan (channel) is not created/open"
        func = self.chan.read
        if stderr:
            func = self.chan.read_stderr
        size, tmp_buf = func(buff_size)
        assert isinstance(self.timeout, (int, float)), "timeout is not either float or int"
        time_end = time.time() + float(self.timeout) / 1000
        while size == LIBSSH2_ERROR_EAGAIN:
            wait_socket(self.sock, self.session, timeout=int(float(self.timeout) / 1000))
            size, tmp_buf = func(buff_size)
            if time.time() > time_end:
                raise NetSsh2Timeout
        return size, tmp_buf

    def _execute_function(self, func, **kwargs):
        """
        Executes any ssh function when the socket is not blocked (LIBSSH2_ERROR_EAGAIN)
        :param func: pointer to function to be executed
        :type func: function

        :param kwargs: any kwargs to be passed to the function

        :return: Anything the function returns
        :rtype: type(ret of function)
        """
        ret = func(**kwargs)
        while ret == LIBSSH2_ERROR_EAGAIN:
            wait_socket(self.sock, self.session)
            ret = func(**kwargs)
        return ret

    def _execute(self, command):
        """
        Wrapper for chan.execute to take keyword argument
        :param command: command to execute on the channel
        :type command: string

        :return: output of ssh2.channel.execute
        :rtype: int
        """
        assert self.chan, "chan (channel) is not created/open"
        return self.chan.execute(command)

    def _clear_buffers(self):
        """
        Clears internal buffers for channel reading
        :return: True
        :rtype: bool
        """
        self.stdout = ""
        self.stderr = ""
        self.stdout_buff = ""
        self.stderr_buff = ""
        return True

    def read_stdout(self):
        """
        Reads 1024 chars from channel STDOUT.
        :return: size of buffer that was read
        :rtype: int
        """
        size, self.stdout_buff = self.read_chan(buff_size=1024)
        self.stdout += self.stdout_buff.decode('ascii', 'ignore')
        return size

    def read_stderr(self):
        """
        Reads 1024 chars from channel STDERR.
        :return: size of buffer that was read
        :rtype: int
        """
        size, self.stderr_buff = self.read_chan(buff_size=1024)
        self.stderr += self.stderr_buff.decode('ascii', 'ignore')
        return size

    def send_cmd(self, cmd):
        """
        Sends command over ssh2 channel.
        :param cmd: command to send
        :type cmd: string

        :raises:  netssh2.exceptions.NetSsh2Timeout in case of timeout

        :return: True
        :rtype: bool
        """
        assert isinstance(cmd, type("")), "cmd (command) is not string"
        assert self.chan, "chan (channel) is not created/open"

        if self.verbose:
            logger().info("Running ssh command '%s'", cmd)

        if self.invoke_shell:
            # send command with newline symbol
            self.chan.write(cmd + self.newline)
            return True

        try:
            self._execute_function(self._execute, command=cmd)
        except NetSsh2Timeout:
            raise NetSsh2Timeout("ssh - Got timeout (%s ms) while executing command: '%s'" % (self.timeout, cmd))
        except Exception as exception:
            logger().error("ssh - Could not execute command: '%s'", cmd)
            logger().error("Failed due: %s", repr(exception))
            raise
        finally:
            self._execute_function(self.chan.close)
        return True

    def wait_prompt(self):
        """
        Keep reading channel until we get prompt.
        :return: True
        :rtype: bool
        """
        # read until we get prompt again
        while not (self.stdout.endswith(self.command_prompt) or self.stdout.endswith(self.prompt)):
            try:
                _, self.stdout_buff = self.read_chan(buff_size=1024)
            except NetSsh2Timeout:
                logger().error("Reading STDOUT timed out after %s ms, did not get prompt '%s'.", self.timeout,
                               self.command_prompt)
                self.stdout_buff = self.command_prompt
            self.stdout += self.stdout_buff if isinstance(self.stdout_buff, type("")) else \
                self.stdout_buff.decode('ascii', 'ignore')
        # Add newline at the end to prevent the above while condition to be True before reading some data
        self.stdout += "\n"
        return True

    def read_output(self):
        """
        Reads output of the command we sent.
        :return: True
        :rtype: bool
        """
        # If there is prompt, we have to wait for it before being able to read the channel
        if self.prompt:
            self.wait_prompt()
        else:
            # Read until we do not receive more bytes. First STDOUT, than STDERR
            size = 1
            while size > 0:
                try:
                    size = self.read_stdout()
                except NetSsh2Timeout:
                    logger().error("Reading STDOUT ssh channel timed out after %s ms.", self.timeout)
                    size, self.stdout_buff = (0, "")
            size = 1
            while size > 0:
                try:
                    size = self.read_stderr()
                except NetSsh2Timeout:
                    logger().warning("Reading STDERR ssh channel timed out after %s ms.", self.timeout)
                    size, self.stderr_buff = (0, "")
        return True

    def run_cmd(self, cmd, return_output=False):
        """
        Run a command to a specific ssh session
        :param cmd: command to run over ssh
        :type cmd: string

        :param return_output: Should we return also output
        :type return_output: bool

        :return: exit_status of command or (exit_status, output) in case of return_output=True
        :rtype: int or tuple(int, str)
        """
        self._clear_buffers()

        # if not using invoke shell, use new channel for every command for speed
        if not self.invoke_shell:
            self.open_channel()
            self.configure_channel()

        self.send_cmd(cmd)
        try:
            self.read_output()
        except SocketRecvError:
            # Socket was closed, this happens when for example we reboot the server by this command
            pass

        # merge STDOUT and STDERR
        self.stdout += self.stderr
        if self.verbose:
            print(self.stdout)

        # Close channel at the end
        if not self.invoke_shell:
            self._execute_function(self.chan.close)
        exit_status = self._execute_function(self.chan.get_exit_status)

        if return_output:
            return exit_status, self.stdout

        return exit_status
