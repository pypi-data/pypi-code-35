import os
import socketserver
import json
import time

from consul import Check
from consul import Consul
from http.server import SimpleHTTPRequestHandler
from logger import logger
from threading import Thread


class HealthServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(bytes(json.dumps({"status": "ok"}), 'utf8'))

        return json.dumps({"status": "OK"})


class AppNotRegisteredException(Exception):
    def __str__(self):
        return 'This service is not registered in discovery server'


class Discovery:

    def __init__(self, host, port):

        self._client = Consul(host=host,
                              port=port)

    @staticmethod
    def parse_health(host, port, endpoint, interval=10, is_https=False):
        """
        Return a dict with health checking information
        """

        if is_https:
            http_string = 'https://'
        else:
            http_string = 'http://'

        url = os.path.join(http_string + host + ':' + str(port), endpoint)

        logger.debug(f'Check url: {url}')

        return Check.http(url, interval)

    @staticmethod
    def up_http_server(host, port, endpoint='/manage/health'):
        """
        Create a child thread with http server registered in
        host:port
        """

        httpd = socketserver.TCPServer((host, port), HealthServer)
        httpd.path = endpoint

        server_thread = Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()

    def verify_service_health(self, app_name):
        """
        Verify is consul service is running
        """

        checks = self._client.agent.checks()[app_name]['Status']

        return checks == 'passing'

    def _verify_service_health_loop(self, app_name, check):
        """
        Reregister the app if that app is not in catalog
        """

        while True:
            if self.verify_service_health(app_name):

                logger.debug('Registering app again')

                self._client.agent.service.deregister(app_name)
                self._client.agent.service.register(app_name, check=check)

                logger.debug('App registered')
            else:
                time.sleep(10)

    def register_app(self, app_name, check):
        """
        Register a app with service_id equal of app_name, in a consul
        agent it's impossible use the same service_id take care of it.
        """

        response = self._client.agent.service.register(app_name, check=check)

        daemon_thread = Thread(target=self._verify_service_health_loop,
                               args=(app_name, check),
                               daemon=True)
        daemon_thread.start()

        return response

    def remove_app(self, service_id):
        """
        Remove a app from catalog and return a boolean
        """

        response = self._client.agent.service.deregister(service_id)

        return response

    def search_app(self, app_name):

        catalog_services = self._client.catalog.service(app_name)

        try:
            service_content = catalog_services[1][0]
        except IndexError:
            raise AppNotRegisteredException()

        host = service_content['ServicePort']
        port = service_content['ServiceAddress']

        adress = {'host': host,
                  'port': port}

        return adress
