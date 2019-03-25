import pprint
import logging
from hippodamia.enums import ViewDetails
from hippodamia.flask.serverthread import ServerThread
from threading import Thread
from flask import Flask, render_template
from flask_basicauth import BasicAuth
from flask.logging import default_handler
from pelops.mylogger import get_child


class FlaskServer:
    _app = None
    _config = None
    _basic_auth = None
    _server_thread = None
    _port = None
    _logger = None

    _shadows = None
    _hierarchical_view = None
    _heartbeat = None
    _onboarding = None
    _full_config = None
    _mqtt_client = None
    _request_ping = None
    _request_runtime = None
    _request_config = None
    _request_reonboarding = None
    _request_end = None

    def __init__(self, config, logger, shadows, heartbeat, hierarchical_view, onboarding, request_ping, request_runtime,
                 request_config, request_reonboarding, request_end, full_config, mqtt_client):
        self._config = config
        self._logger = get_child(logger, self.__class__.__name__, self._config)
        self._logger.addHandler(default_handler)
        self._logger.info("__init__ - start")
        self._logger.debug("__init__ - config: {}".format(self._config))

        self._shadows = shadows
        self._hierarchical_view = hierarchical_view
        self._heartbeat = heartbeat
        self._onboarding = onboarding
        self._request_ping = request_ping
        self._request_runtime = request_runtime
        self._request_config = request_config
        self._request_reonboarding = request_reonboarding
        self._request_end = request_end
        self._full_config = full_config
        self._mqtt_client = mqtt_client

        self._port = self._config["port"]

        self._app = Flask(__name__)
        self._basic_auth = self._create_basic_auth()
        self._add_routes()

        self._logger.info("__init__ - finished")

    def _create_basic_auth(self):
        if "username" in self._config and "password" in self._config:
            self._logger.info("_create_basic_auth - adding basic_auth")
            self._app.config['BASIC_AUTH_USERNAME'] = self._config["username"]
            self._app.config['BASIC_AUTH_PASSWORD'] = self._config["password"]
            self._app.config['BASIC_AUTH_FORCE'] = True
            return BasicAuth(self._app)
        else:
            self._logger.info("_create_basic_auth - skipping")
            return None

    def _run_server(self):
        self._logger.debug("app.run")
        self._app.run(port=self._port)

    def start(self):
        self._logger.info("starting flask server in process")
        self._server_thread = ServerThread(self._app, self._port)
        self._server_thread.start()
        self._logger.info("flask server started")

    def stop(self):
        self._logger.info("terminating flask server process")
        self._server_thread.stop()
        self._server_thread.join()
        self._logger.info("flask server stopped")

    def _add_routes(self):
        self._logger.debug("adding routes")
        self._app.add_url_rule('/', view_func=self.route_index)
        self._app.add_url_rule('/hierarchical', view_func=self.route_service_hierarchical)
        self._app.add_url_rule('/list', view_func=self.route_service_list)
        self._app.add_url_rule('/heartbeatstats', view_func=self.route_heartbeatstats)
        self._app.add_url_rule('/onboardingstats', view_func=self.route_onboardingstats)
        self._app.add_url_rule('/service/<gid>/commands', view_func=self.route_service_commands)
        self._app.add_url_rule('/service/<gid>/details', view_func=self.route_service_details)
        self._app.add_url_rule('/service/<gid>/logs', view_func=self.route_service_logs)
        self._app.add_url_rule('/mqtt_stats', view_func=self.route_mqtt_stats)
        self._app.add_url_rule('/show_config', view_func=self.route_show_config)
        self._app.add_url_rule('/service/<gid>/commands/<cmd>', view_func=self.execute_commands)

    def route_index(self):
        return render_template('index.html', name="test")

    def route_service_hierarchical(self):
        # output = self._hierarchical_view.pformat(details=ViewDetails.FULL)
        # title = "Hierarchical View"
        # return render_template('pre.html', title=title, content=output)
        title = "Hierarchical View"
        return render_template('hierarchical_view.html', title=title, tree=self._hierarchical_view.tree)

    def route_service_list(self):
        return render_template('service_list.html', service_list=self._shadows)

    def route_heartbeatstats(self):
        output = "heartbeat: \n"
        output += " - counter: {}\n".format(self._heartbeat.counter)
        output += " - last timestamp: {}\n".format(self._heartbeat.last_timestamp)
        output += " - interval: {} s\n".format(self._heartbeat.interval)
        output += " - topic: {}\n".format(self._heartbeat.topic)
        title = "Heartbeat Statistics"
        return render_template('pre.html', title=title, content=output)

    def route_onboardingstats(self):
        output = "onboarding: \n"
        output += " - counter: {}\n".format(self._onboarding.counter)
        output += " - gid_list: {}\n".format(self._onboarding.gid_list)
        output += " - enforcement: {}\n".format(self._onboarding.enforcement.name)
        output += " - protocol_version: {}\n".format(self._onboarding.protocol_version)
        output += " - topic_onboarding_request: {}\n".format(self._onboarding.topic_onboarding_request)
        output += " - last_timestamp: {}\n".format(self._onboarding.last_timestamp)
        output += " - last_message: \n"
        output += pprint.pformat(self._onboarding.last_message, indent=4)
        title = "Onboarding Statistics"
        return render_template('pre.html', title=title, content=output)

    def route_service_commands(self, gid):
        try:
            stats = self._shadows[gid].overall_stats()
        except KeyError:
            return render_template('pre.html', title="Service Commands", content="unknown gid '{}'".format(gid))

        return render_template('commands.html', title="Service Commands for '{}'".format(gid), gid=gid)

    def execute_commands(self, gid, cmd):
        try:
            stats = self._shadows[gid].overall_stats()
        except KeyError:
            return render_template('pre.html', title="Service Commands", content="unknown gid '{}'".format(gid))

        message = "executed command '{}'".format(cmd)
        cmd = cmd.lower()
        if cmd == "request_ping":
            self._request_ping(gid)
        elif cmd == "request_runtime":
            self._request_runtime(gid)
        elif cmd == "request_config":
            self._request_config(gid)
        elif cmd == "request_reonboarding":
            self._request_reonboarding(gid)
        elif cmd == "request_end":
            self._request_end(gid)
        else:
            message = "unknown command '{}'".format(cmd)

        return render_template('commands.html', title="Service Commands for '{}'".format(gid), gid=gid, message=message)

    def route_service_details(self, gid):
        try:
            stats = self._shadows[gid].overall_stats()
        except KeyError:
            return render_template('pre.html', title="Service Details", content="unknown gid '{}'".format(gid))

        pre_stats = {}
        for k, v in stats.items():
            pre_stats[k] = pprint.pformat(v, indent=4)

        return render_template('details_pre.html', title="Service Details for '{}'".format(gid), gid=gid,
                               content=pre_stats)

    def route_service_logs(self, gid):
        try:
            shadow = self._shadows[gid]
        except KeyError:
            return render_template('pre.html', title="Service Logs", content="unknown gid '{}'".format(gid))

        temp = {
            "merged list": shadow.shadow_data.logger.flat_list,
            "DEBUG": shadow.shadow_data.logger.level_dict[logging.DEBUG],
            "INFO": shadow.shadow_data.logger.level_dict[logging.INFO],
            "WARNING": shadow.shadow_data.logger.level_dict[logging.WARNING],
            "ERROR": shadow.shadow_data.logger.level_dict[logging.ERROR],
            "CRITICAL": shadow.shadow_data.logger.level_dict[logging.CRITICAL],
        }

        pre_logs = {}
        for k, shadow_logger in temp.items():
            output = "received: {}, stored: {}\n".format(shadow_logger.counter, len(shadow_logger.log))
            counter = shadow_logger.counter
            for l in shadow_logger.log:
                output += "{}: {}\n".format(counter, pprint.pformat(l, indent=4))
                counter -= 1
            if counter > 0:
                output += "-- skipping {} removed log-entries".format(counter)
            pre_logs[k] = output

        return render_template('logs_pre.html', title="Service Logs for '{}'".format(gid), gid=gid, content=pre_logs)

    def route_mqtt_stats(self):
        text = "mqtt client connection active: {}\n".format(self._mqtt_client.is_connected.is_set())
        text += "active subscriptions:\n"
        for sub, func in self._mqtt_client.subscribed_topics().items():
            text += " - {}: [{}]\n".format(sub, func)
        text += "send/receive statistics: \n"
        text += self._mqtt_client.stats.generate_overview()
        title = "MQTT Statistics"
        return render_template('pre.html', title=title, content=text)

    def route_show_config(self):
        text = pprint.pformat(self._full_config, indent=2)
        title = "Config"
        return render_template('pre.html', title=title, content=text)




