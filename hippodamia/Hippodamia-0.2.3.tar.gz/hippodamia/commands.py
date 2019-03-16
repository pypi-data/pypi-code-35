import pprint
import datetime
import pelops.ui.tools
from hippodamia.enums import StatType
from hippodamia.enums import ViewDetails
import logging


class CommandFactory:
    _logger = None
    _shadows = None
    _hierarchical_view = None
    _request_ping = None
    _request_runtime = None
    _request_config = None
    _request_reonboarding = None
    _request_end = None
    _stop_service = None
    _heartbeat = None
    _onboarding = None
    _config = None

    def __init__(self, version, config, shadows, heartbeat, health_view, onboarding, request_ping, request_runtime,
                 request_config, request_reonboarding, request_end, stop_service, logger):
        self._shadows = shadows
        self._config = config
        self._hierarchical_view = health_view
        self._request_ping = request_ping
        self._request_runtime = request_runtime
        self._request_config = request_config
        self._request_reonboarding = request_reonboarding
        self._request_end = request_end
        self._stop_service = stop_service
        self._logger = logger
        self._heartbeat = heartbeat
        self._onboarding = onboarding

    def add_commands(self, add_command):
        add_command("request_ping", self.do_request_ping)
        add_command("request_runtime", self.do_request_runtime)
        add_command("request_config", self.do_request_config)
        add_command("request_reonboarding", self.do_request_reonboarding)
        add_command("request_end", self.do_request_end)
        add_command("list", self.do_list)
        add_command("hierarchical", self.do_hierarchical)
        add_command("agentstats", self.do_agentstats)
        add_command("agentlog", self.do_agentlog)
        add_command("heartbeatstats", self.do_heartbeatstats)
        add_command("onboardingstats", self.do_onboardingstats)
        add_command("a", self.do_a)
        add_command("g", self.do_g)
        add_command("h", self.do_h)
        add_command("l", self.do_l)
        add_command("o", self.do_o)

    def _check_gid(self, gid):
        if gid not in self._shadows:
            raise KeyError("gid {} not in {}".format(gid, self._shadows.keys()))
        return gid

    def _request_extract_gid(self, name, arg):
        args = pelops.ui.tools.parse(arg)

        gid = None
        if len(args) == 1 and str(args[0]).lower() == "all":
            print("Sending {} request to all monitored services\n".format(name))
        elif len(args) == 2 and str(args[0]).lower() == "gid":
            gid = self._check_gid(args[1])
            print("Send {} regest to monitoring service with gid == {}\n".format(name, gid))
        else:
            raise ValueError("Wrong arguments: {}. expected '{} [all|gid gid]'.\n".format(args, name))

        return gid

    def do_exit(self, arg):
        """exit - stops the monitoring service: EXIT"""
        return True

    def do_request_ping(self, arg):
        """request_ping [all|gid gid] - publish ping request either to all monitored services or to a specific one: REQUEST_PING GID 1"""
        try:
            self._request_ping(self._request_extract_gid("ping", arg))
        except (KeyError, ValueError) as e:
            print("{}\n".format(e))

    def do_request_runtime(self, arg):
        """request_runtime [all|gid gid] - publish runtime request either to all monitored services or to a specific one: REQUEST_RUNTIME GID 1"""
        try:
            self._request_runtime(self._request_extract_gid("runtime", arg))
        except (KeyError, ValueError) as e:
            print("{}\n".format(e))
            
    def do_request_config(self, arg):
        """request_config [all|gid gid] - publish config request either to all monitored services or to a specific one: REQUEST_CONFIG GID 1"""
        try:
            self._request_config(self._request_extract_gid("config", arg))
        except (KeyError, ValueError) as e:
            print("{}\n".format(e))
            
    def do_request_reonboarding(self, arg):
        """request_reonboarding [all|gid gid] - publish reonboarding request either to all monitored services or to a specific one: REQUEST_REONBOARDING GID 1"""
        try:
            self._request_reonboarding(self._request_extract_gid("reonboarding", arg))
        except (KeyError, ValueError) as e:
            print("{}\n".format(e))
            
    def do_request_end(self, arg):
        """request_end [all|gid gid] - publish end request either to all monitored services or to a specific one: REQUEST_END GID 1"""
        try:
            self._request_end(self._request_extract_gid("end", arg))
        except (KeyError, ValueError) as e:
            print("{}\n".format(e))

    def do_list(self, arg):
        """list - list all known services: LIST"""
        m = ""
        for gid, shadow in self._shadows.items():
            m += "gid: {}, state: {}, health:{}, necessity: {}, name: {}\n"\
                .format(gid, shadow.get_state_id().name, shadow.properties.health.name,
                        shadow.properties.necessity.name, shadow.properties.name)
        pelops.ui.tools.more(m)

    def do_hierarchical(self, arg):
        """hierarchical [location location|room room|device device|service service]*
 - show all monitored services: HIERARCHICAL
 - show one location: HIERARCHICAL LOCATION Flat
 - show one specific service: HIERARCHICAL LOCATION Flat ROOM \"Living Room\" DEVICE Thermostat SERVICE \"Thermostat GUI\"
 - show all service that run on devices with the name 'Thermostat': HIERARCHICAL DEVICE Thermostat"""
        syntax = "hierarchical [location location|room room|device device|service service]*"
        arguments = pelops.ui.tools.parse(arg)
        if len(arguments) % 2 == 1:
            print("wrong number of arguments ({}). expected '{}'".format(len(arguments), syntax))
            return
        elif len(arguments) == 0:
            m = self._hierarchical_view.pformat(details=ViewDetails.FULL)
        else:
            filters = {"LOCATION": "", "ROOM": "", "DEVICE": "", "SERVICE": ""}
            pos = 0
            while pos < len(arguments):
                first = arguments[pos].upper()
                second = arguments[pos+1]
                if first in filters:
                    filters[first] = second
                else:
                    print("don't know a parameter/filter named '{}'. expected '{}'".format(first, syntax))
                    return
                pos += 2
            m = self._hierarchical_view.pformat(details=ViewDetails.FULL, filters=filters)
        pelops.ui.tools.more(m)

    def do_agentstats(self, arg):
        """agentstats gid gid [all|general|properties|ping|runtime|config|request|logger]
        show information on one specific monitored service: AGENTSTATS GID 1 PROPERTIES"""
        syntax = "agentstats gid gid [all|general|properties|ping|runtime|config|request|logger]"

        args = pelops.ui.tools.parse(arg)
        if len(args) != 3:
            print("wrong number of arguments: {}. expected '{}'\n".format(args, syntax))
        elif str(args[0]).lower() != "gid":
            print("first argument ({}) must be 'gid'. expected '{}'\n".format(str(args[0]).lower(), syntax))
        elif str(args[2]).upper() not in StatType.get_members():
            print("third argument ({}) must be one of {}. expected '{}'\n".format(str(args[2]).lower(),
                                                                                  StatType.get_members(), syntax))
        else:
            try:
                stat_type = StatType.get_enum(str(args[2]))
                gid = self._check_gid(args[1])
                self._print_stats(gid, stat_type)
            except (ValueError, KeyError) as e:
                print("{}\n".format(e))

    def _print_stats(self, gid, type):
        print("stats {} for gid {}:\n".format(type, gid))

        shadow = self._shadows[gid]
        output = ""

        if type == StatType.GENERAL or type == StatType.ALL:
            output += "general: \n"
            output += " - active_state:\n"
            output += "   - name: {}\n".format(shadow.get_state_id().name)
            since = shadow.states[shadow.get_state_id()].timestamp_on_entry
            output += "   - since: {}\n".format(since)
            try:
                output += "   - duration: {}\n".format(datetime.datetime.now()-since)
            except TypeError:
                pass  # since is of type None
            output += " - machine state states: \n"
            for id, state in shadow.states.items():
                try:
                    duration = state.timestamp_on_exit - state.timestamp_on_entry
                except TypeError:
                    try:
                        duration = datetime.datetime.now() - state.timestamp_on_entry
                    except TypeError:
                        duration = "-"

                output += "   - {}: on_entry {} @{}, on_exit {} @{}, duration {}\n"\
                    .format(id.name, state.counter_on_entry, state.timestamp_on_entry,
                            state.counter_on_exit, state.timestamp_on_exit, duration)
            output += " - message stats: \n"
            for id, counter in shadow.shadow_data.get_counter_dict().items():
                output += "   - {}: {}\n".format(id, counter)
            output += " - topics: \n"
            for id, topic in shadow.activity_topics.items():
                output += "   - {}: {}\n".format(id, topic)
            output += " - timings: \n"
            for id, timing in shadow.service_timings.items():
                output += "   - {}: {}\n".format(id, timing)

        if type == StatType.PROPERTIES or type == StatType.ALL:
            output += "properties: @{}\n".format(shadow.shadow_data.properties_time)
            output += pprint.pformat(shadow.shadow_data.properties, indent=4)
            output += "\n"

        if type == StatType.PING or type == StatType.ALL:
            output += "ping: #{} @{}\n".format(shadow.shadow_data.ping_counter, shadow.shadow_data.ping_time)
            output += pprint.pformat(shadow.shadow_data.ping, indent=4)
            output += "\n"

        if type == StatType.RUNTIME or type == StatType.ALL:
            output += "runtime: #{} @{}\n".format(shadow.shadow_data.runtime_counter, shadow.shadow_data.runtime_time)
            output += pprint.pformat(shadow.shadow_data.runtime, indent=4)
            output += "\n"

        if type == StatType.CONFIG or type == StatType.ALL:
            output += "config: #{} @{}\n".format(shadow.shadow_data.config_counter, shadow.shadow_data.config_time)
            output += pprint.pformat(shadow.shadow_data.config, indent=4)
            output += "\n"

        if type == StatType.REQUEST or type == StatType.ALL:
            output += "request: #{} @{}\n".format(shadow.shadow_data.request_counter, shadow.shadow_data.request_time)
            output += pprint.pformat(shadow.shadow_data.request, indent=4)
            output += "\n"

        if type == StatType.LOGGER or type == StatType.ALL:
            output += "logger:\n"
            output += "  max-level: {}\n".format(shadow.shadow_data.logger.max_level)
            output += "  combined list: {}\n".format(shadow.shadow_data.logger.flat_list.stats())
            output += "  CRITICAL: {}\n".format(shadow.shadow_data.logger.level_dict[logging.CRITICAL].stats())
            output += "  ERROR: {}\n".format(shadow.shadow_data.logger.level_dict[logging.ERROR].stats())
            output += "  WARNING: {}\n".format(shadow.shadow_data.logger.level_dict[logging.WARNING].stats())
            output += "  INFO: {}\n".format(shadow.shadow_data.logger.level_dict[logging.INFO].stats())
            output += "  DEBUG: {}\n".format(shadow.shadow_data.logger.level_dict[logging.DEBUG].stats())

        if output == "":
            print("Factory._print_stats: unknown stat type '{}'\n".format(type))
        else:
            pelops.ui.tools.more(output)

    def do_agentlog(self, arg):
        """agentlog gid gid [FLAT|DEBUG|INFO|WARNING|ERROR|CRITICAL] - view all received log-entries of this
service: AGENTLOG GID 1 FLAT"""
        syntax = "agentlog gid gid [FLAT|DEBUG|INFO|WARNING|ERROR|CRITICAL]"

        args = pelops.ui.tools.parse(arg)
        if len(args) != 3:
            print("wrong number of arguments: {}. expected '{}'\n".format(args, syntax))
        elif str(args[0]).lower() != "gid":
            print("first argument ({}) must be 'gid'. expected '{}'\n".format(str(args[0]).lower(), syntax))
        elif str(args[2].lower()) not in ["flat", "debug", "info", "warning", "error", "critical"]:
            print("unexpected value for third argument '{}'. expected '{}'\n".format(args[2], syntax))
        else:
            gid = self._check_gid(args[1])
            shadow = self._shadows[gid]
            output = "show log for gid: {}\n".format(gid)

            shadow_logger = None
            if args[2].lower() == "flat":
                shadow_logger = shadow.shadow_data.logger.flat_list
            elif args[2].lower() == "debug":
                shadow_logger = shadow.shadow_data.logger.level_dict[logging.DEBUG]
            elif args[2].lower() == "info":
                shadow_logger = shadow.shadow_data.logger.level_dict[logging.INFO]
            elif args[2].lower() == "warning":
                shadow_logger = shadow.shadow_data.logger.level_dict[logging.WARNING]
            elif args[2].lower() == "error":
                shadow_logger = shadow.shadow_data.logger.level_dict[logging.ERROR]
            elif args[2].lower() == "critical":
                shadow_logger = shadow.shadow_data.logger.level_dict[logging.CRITICAL]
            else:
                raise ValueError("do_agentlog - unknown argument value '{}'".format(args[2]))

            output += "received: {}, stored: {}\n".format(shadow_logger.counter, len(shadow_logger.log))
            counter = shadow_logger.counter
            for l in shadow_logger.log:
                output += "{}: {}\n".format(counter, pprint.pformat(l, indent=4))
                counter -= 1
            if counter > 0:
                output += "-- skipping {} removed log-entries".format(counter)
            pelops.ui.tools.more(output)

    def do_heartbeatstats(self, arg):
        """heartbeatstats - stats on the heartbeat signal of the monitoring agent: HEARTBEATSTATS"""
        output = "heartbeat: \n"
        output += " - counter: {}\n".format(self._heartbeat.counter)
        output += " - last timestamp: {}\n".format(self._heartbeat.last_timestamp)
        output += " - interval: {} s\n".format(self._heartbeat.interval)
        output += " - topic: {}\n".format(self._heartbeat.topic)
        pelops.ui.tools.more(output)

    def do_onboardingstats(self, arg):
        """onboardingstats - stats on the overall onboarding process: ONBOARDINGSTATS"""
        output = "onboarding: \n"
        output += " - counter: {}\n".format(self._onboarding.counter)
        output += " - gid_list: {}\n".format(self._onboarding.gid_list)
        output += " - enforcement: {}\n".format(self._onboarding.enforcement.name)
        output += " - protocol_version: {}\n".format(self._onboarding.protocol_version)
        output += " - topic_onboarding_request: {}\n".format(self._onboarding.topic_onboarding_request)
        output += " - last_timestamp: {}\n".format(self._onboarding.last_timestamp)
        output += " - last_message: \n"
        output += pprint.pformat(self._onboarding.last_message, indent=4)
        pelops.ui.tools.more(output)

    def do_config(self, arg):
        """config - show the current config: CONFIG"""
        output = pprint.pformat(self._config, indent=2)
        pelops.ui.tools.more(output)

    def do_a(self, arg):
        # """shortcut for 'stats gid 1 all'"""
        self._print_stats("1", StatType.ALL)

    def do_g(self, arg):
        # """shortcut for 'stats gid 1 general'"""
        self._print_stats("1", StatType.GENERAL)

    def do_h(self, arg):
        # """shortcut for 'hierarchical'"""
        self.do_hierarchical(arg)

    def do_l(self, arg):
        # """shortcut for 'list'"""
        self.do_list(arg)

    def do_o(self, arg):
        # """ shortcut for 'onboardingstats'"""
        self.do_onboardingstats(arg)
