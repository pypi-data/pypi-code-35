import argparse
import json
import threading
import datetime
import pprint
from pelops import mylogger
from pelops import myconfigtools
from pelops.mymqttclient import MyMQTTClient
import pelops.schema.abstractmicroservice
from hippodamia_agent.monitoringagent import MonitoringAgent
from pelops.ui.ui import UI
import pelops.ui.tools


class AbstractMicroservice:
    """
    Base class for all MicroServices of pelops. Takes care of reading and validating the config, providing mymqttclient
    and logger instances as well as static methods to create an instance and run it indefinitly.

    If no mqtt client has been provided, the config must have an "mqtt" entry at root level. Same accounts for the
    logger.

    An implementation of this abstract class should use the provided config, mqtt_client, and logger. But most
    importantly, it must adhere to the _is_stopped and _stop_service Events and make good use of the _start and
    _stop methods. Otherwise, starting and stopping the microservice might not be possible in the framework.

    The two events/flags _is_started and _is_stopped show the state of the Service. They are changed in the methods
    start and stop. During the start and the stopped sequences, both events are cleared. Thus, in case of an error
    during these sequences, the state of the microservice is undefined.
    """

    _config = None  # config yaml structure
    _full_config = None  # config ymal structure of the full config file (not only parts for this service)
    _is_stopped = None  # event that is True if the service is not running
    _is_started = None  # event that is True if the service is running
    _stop_service = None  # event that must be used by all internal loops. if evet fires, they must stop.
    _startstop_lock = None  # lock start/stop routine - prevents from interrupting an ongoing start/stop process
    _asyncstart_thread = None  # thread for asnychronous start
    _asyncstop_thread = None  # thread for asynchronous stop
    _mqtt_client = None  # mymqttclient instance
    _logger = None  # logger instance
    _stop_mqtt_client = None  # if mqtt_client has been created by this instance, it should be shutdown as well
    _monitoring_agent = None  # hippodamia agent
    _UI = None  # cmd.cmd instance
    _manage_ui = None  # whether _UI is controlled (created, started, stopped) by this instance or not

    def __init__(self, config, config_class_root_node_name,
                 mqtt_client=None, logger=None, logger_name=None,
                 manage_monitoring_agent=True, stdout_log_level="WARNING", no_gui=False):
        """
        Constructor

        :param config: config yaml structure
        :param config_class_root_node_name: string - name of root node of microservice config
        :param mqtt_client: mymqttclient instance
        :param logger: logger instance - optional
        :param logger_name: name for logger instance - optional
        :param manage_monitoring_agent: create and control a hippodamia-agent instance
        :param no_gui: if False create and control a ui instance
        :param stdout_log_level: if set, a logging handler with target sys.stdout will be added
        """
        if stdout_log_level is None:
            stdout_log_level = "WARNING"
        if no_gui is None:
            no_gui = False

        self._config = config[config_class_root_node_name]
        self._full_config = config

        if logger_name is None:
            logger_name = __name__

        if logger is None:
            self._logger = mylogger.create_logger(config["logger"], logger_name)
            mylogger.add_log2stdout_handler(self._logger, stdout_log_level)
        else:
            self._logger = logger.getChild(logger_name)

        self._logger.info("{}.__init__ - initializing".format(self.__class__.__name__))
        self._logger.debug("{}.__init__ - config: {}".format(self.__class__.__name__, self._config))

        self._is_stopped = threading.Event()
        self._is_stopped.set()
        self._is_started = threading.Event()
        self._is_started.clear()

        self._stop_service = threading.Event()
        self._stop_service.clear()

        self._startstop_lock = threading.Lock()
        self._asyncstart_thread = threading.Thread(target=self.start)
        self._asyncstop_thread = threading.Thread(target=self.stop)

        self._manage_ui = not no_gui

        if mqtt_client is None:
            self._mqtt_client = MyMQTTClient(config["mqtt"], self._logger)
            self._stop_mqtt_client = True
            self._add_ui_command("mqtt_stats", self._cmd_mqtt_stats)
            self._add_ui_command("show_config", self._cmd_show_config)
        else:
            self._mqtt_client = mqtt_client
            self._stop_mqtt_client = False

        if manage_monitoring_agent:
            if "monitoring-agent" in config:
                self._monitoring_agent = MonitoringAgent(config["monitoring-agent"], self, self._mqtt_client,
                                                         self._logger)
                self._check_log_level_compatibility()
                self._add_ui_command("monitoring_runtime_info", self._cmd_monitoring_agent_runtime_info)
                self._add_ui_command("monitoring_config_info", self._cmd_monitoring_agent_config_info)
                self._add_ui_command("monitoring_state", self._cmd_monitoring_agent_state)
                self._add_ui_command("monitoring_restart", self._cmd_monitoring_agent_restart)
                self._add_ui_command("monitoring_timings", self._cmd_monitoring_agent_timings)

        self._logger.info("{}.__init__ - AbstractMicroservice done".format(self.__class__.__name__))

    def _cmd_monitoring_agent_restart(self, args):
        """monitoring_restart - restart the monitoring agent / re-onboard (monitoring agent): MONITORING_RESTART"""
        pelops.ui.tools.more("... restarting monitoring agent")
        self._monitoring_agent.restart()

    def _cmd_monitoring_agent_timings(self, args):
        """monitoring_timings - list the current timing setting: MONITORING_TIMINGS"""
        text = pprint.pformat(self._monitoring_agent.timings, indent=2)
        pelops.ui.tools.more(text)

    def _cmd_monitoring_agent_runtime_info(self, args):
        """runtime_info - show the current runtime info (monitoring agent): RUNTIME_INFO"""
        struct = json.loads(self._monitoring_agent.generate_runtime_message())
        text = pprint.pformat(struct, indent=2)
        pelops.ui.tools.more(text)

    def _cmd_monitoring_agent_config_info(self, args):
        """runtime_info - show the current runtime info (monitoring agent): RUNTIME_INFO"""
        struct = json.loads(self._monitoring_agent.generate_config_message())
        text = pprint.pformat(struct, indent=2)
        pelops.ui.tools.more(text)

    def _cmd_monitoring_agent_state(self, args):
        """onboarding_state - show the current onboarding state (monitoring agent): ONBOARDING_STATE"""
        entry = self._monitoring_agent.state_history[-1]
        diff = datetime.datetime.now() - entry.datetime
        text = "current state: {}, active for {} s.({})\n".\
            format(entry.state, diff, self._monitoring_agent.current_state().__class__.__name__)
        text += "state history (maximum last {} entries):\n".format(self._monitoring_agent.state_history.maxlen)
        for entry in self._monitoring_agent.state_history:
            text += " - {} / {}\n".format(entry.datetime.strftime("%Y/%m/%d-%H:%M:%S.%f"), entry.state)
        pelops.ui.tools.more(text)

    def _cmd_mqtt_stats(self, args):
        """mqtt_stats - show the mqtt client statistics (mqtt client): MQTT_STATS"""
        text = "mqtt client connection active: {}\n".format(self._mqtt_client.is_connected.is_set())
        text += "active subscriptions:\n"
        for sub, func in self._mqtt_client.subscribed_topics().items():
            text += " - {}: [{}]\n".format(sub, func)
        text += "send/receive statistics: \n"
        text += self._mqtt_client.stats.generate_overview()
        pelops.ui.tools.more(text)

    def _cmd_show_config(self, args):
        """config - show the current config: CONFIG"""
        text = pprint.pformat(self._full_config, indent=2)
        pelops.ui.tools.more(text)

    def _check_log_level_compatibility(self):
        if self._monitoring_agent and self._mqtt_client:
            mqtt_log_level = self._mqtt_client._config["log-level"].upper()
            monitoring_log_level = self._monitoring_agent._config["log-level"].upper()
            if (((mqtt_log_level == "INFO") or (mqtt_log_level == "DEBUG")) and
                    ((monitoring_log_level == "INFO") or (monitoring_log_level == "DEBUG"))):
                err = "If mqtt log level ist INFO or DEBUG (currently set to {}) the log level of the " \
                      "monitoring agent _must_ be WARNING or higher (currently set to {})."\
                    .format(mqtt_log_level, monitoring_log_level)
                self._logger.error(err)
                raise ValueError(err)

    def _start(self):
        """abstract start method - to be implemented by child"""
        self._logger.warning("{}._start - NotImplementedError".format(self.__class__.__name__))
        raise NotImplementedError

    def asyncstart(self):
        """start microservice and return immediately (dont wait until start has been finished)"""
        self._logger.info("{} - async start".format(self.__class__.__name__))
        self._asyncstart_thread.start()

    def asyncstop(self):
        """stop microservice and return immediately (dont wait until stop has been finished)"""
        self._logger.info("{} - async stop".format(self.__class__.__name__))
        self._asyncstop_thread.start()

    def start(self):
        """start microservice - resets events, starts mymqttclient, and calls _start."""
        self._logger.warning("{} - starting".format(self.__class__.__name__))
        self._logger.info("{} - starting".format(self.__class__.__name__))
        with self._startstop_lock:
            self._logger.info("{} - start_lock acquired".format(self.__class__.__name__))
            self._is_stopped.clear()
            self._stop_service.clear()
            if not self._mqtt_client.is_connected.is_set():
                self._mqtt_client.connect()
                self._mqtt_client.is_connected.wait()
            else:
                self._logger.info("{} - mqtt_client is already running".format(self.__class__.__name__))
            if self._monitoring_agent:
                self._monitoring_agent.start()
            self._start_ui()
            self._start()
            self._is_started.set()
            self._logger.info("{} - started".format(self.__class__.__name__))

    def _start_ui(self):
        if self._manage_ui:
            intro = "{} v{}\n{}\n   Type help or ? to list commands.\n" \
                .format(self.__class__.__name__, self._version, self._get_description())
            prompt = "({}) ".format(self.__class__.__name__.lower())
            self._UI = UI(intro, prompt, self.stop, self._stop_service)
            self._UI.start()

    def _stop_ui(self):
        if self._manage_ui:
            self._UI.stop()

    def _add_ui_command(self, name, function):
        try:
            UI.add_command(name, function)
        except ValueError as e:
            self._logger.info(e)
        except AttributeError as e:
            self._logger.error(e)

    def _stop(self):
        """abstract stop method - to be implemented by child"""
        self._logger.warning("{}._stop - NotImplementedError".format(self.__class__.__name__))
        raise NotImplementedError

    def stop(self):
        """stop microservice - sets _stop_service event, calls _stop and sets _is_stopped."""
        self._logger.info("{} - stopping".format(self.__class__.__name__))
        with self._startstop_lock:
            self._logger.info("{} - _stop_lock acquired".format(self.__class__.__name__))
            self._is_started.clear()
            self._stop_service.set()
            self._stop_ui()
            self._stop()
            if self._monitoring_agent:
                self._monitoring_agent.stop()
            if self._stop_mqtt_client:
                self._mqtt_client.disconnect()
                self._mqtt_client.is_disconnected.wait()
            self._logger.warning("{} - stopped".format(self.__class__.__name__))
            self._is_stopped.set()
            self._logger.info("{} - stopped".format(self.__class__.__name__))

    def runtime_information(self):
        """
        return runtime information in a dict for logging/monitoring purposes.

        :return: dict / list
        """
        raise NotImplementedError

    def config_information(self):
        """
        return config information in a dict for logging/monitoring purposes.

        :return: dict / list
        """
        raise NotImplementedError

    @classmethod
    def _get_schema(cls):
        """
        Returns the child specific json schema - to be implemented by child.

        :return: json schema struct
        """
        raise NotImplementedError

    @classmethod
    def get_schema(cls):
        return pelops.schema.abstractmicroservice.get_schema(cls._get_schema())

    @classmethod
    def dump_schema(cls, filename):
        """
        Dumps the latest schema to the provided file but only iff the contents differ. If no file is found, a new file
        will be generated.

        :param filename - path to autogenerated config schema json file
        """
        new_schema = json.dumps(cls.get_schema(), indent=4)

        try:
            with open(filename, 'r') as f:
                old_schema = f.read()
        except OSError:
            old_schema = ""

        if new_schema != old_schema:
            print("updating {} to latest schema.".format(filename))
            with open(filename, 'w') as f:
               f.write(new_schema)


    @classmethod
    def _get_description(cls):
        """
        Shortescription of microservice. Used for command line interface output.

        :return: string
        """
        raise NotImplementedError

    @classmethod
    def _get_arguments(cls, args=None):
        """Handle command line arguments and read the yaml file into a json structure (=config)."""
        desc = cls._get_description()
        ap = argparse.ArgumentParser(description=desc)
        ap.add_argument('-c', '--config', type=str, help='yaml config file', required=True)
        ap.add_argument('-q', '--quiet', help='suppress all output (cannot be used together with -v',
                        action='store_true')
        ap.add_argument('-v', '--verbose', help='more output (cannot be used together with -q)',
                        action='store_true')
        ap.add_argument('--no_gui', help='do not start the command gui', action='store_true')
        ap.add_argument('--version', action='version',
                            version='%(prog)s {}'.format(cls._version),
                            help='show the version number and exit')
        if args:
            arguments = vars(ap.parse_args(args))
        else:
            arguments = vars(ap.parse_args())

        config_filename = arguments["config"]
        no_gui = arguments["no_gui"]

        quiet = arguments["quiet"]
        verbose = arguments["verbose"]
        if quiet and verbose:
            raise AttributeError("--quiet and --verbose cannot be used together")
        elif quiet:
            stdout_log_level = ""
        elif verbose:
            stdout_log_level = "INFO"
        else:
            stdout_log_level = "WARNING"

        return config_filename, stdout_log_level, no_gui

    @classmethod
    def _read_config(cls, config_filename):
        config = myconfigtools.read_config(config_filename)
        config = myconfigtools.dict_deepcopy_lowercase(config)
        schema = cls.get_schema()
        validation_result = myconfigtools.validate_config(config, schema)
        if validation_result:
            raise ValueError("Validation of config file failed: {}".format(validation_result))
        return config

    def run(self):
        """
        execution loop - starts, waits infinitely for keyboardinterupt, and stops if this interrupt happend.
        """
        self.start()

        try:
            while not self._is_stopped.wait(0.25):  # timeout is necessary for CTRL+C
                pass
        except KeyboardInterrupt:
            self._logger.info("KeyboardInterrupt")
            self.stop()

    @classmethod
    def standalone(cls, args=None):
        """Public method to start this driver directly. Instantiates an mymqttclient and creates an object for the
                given driver."""
        config_filename, stdout_log_level, no_gui = cls._get_arguments(args)

        config = cls._read_config(config_filename)

        instance = None
        try:
            instance = cls(config, stdout_log_level=stdout_log_level, no_gui=no_gui)
            instance.run()
        except Exception as e:
            if instance is not None and instance._logger is not None:
                instance._logger.exception(e)
            raise

