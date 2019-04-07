from lysidike.services.aservice import AService
import smtplib
from email.mime.text import MIMEText


class EmailService(AService):
    """
    Classic publish to email service.

    config yaml entries:

    email:
            address: smtp.zoho.com  # url of smtp server
            port: 465  # port of smtp server
            from: name123@sender123.com  # sender email address
            to: name123@receiver123.com  # send to email address. either single string or array of strings
            credentials-file: ~/credentials.yaml  # a yaml config file with one root entry as described below

    credentials yaml file:

    publish-gateway:
        services:
            email:
                username: username  # username for smtp server
                password: password  # password for smtp server
    """

    _address = None  # url of smtp server
    _port = None  # port of smtp server
    _username = None  # username for smtp server
    _password = None  # password for smtp server
    _from = None  # sender email address
    _to = None  # send to email address

    def __init__(self, config, mqtt_client, logger):
        """
        Constructor

        :param config: yaml config structure
        :param mqtt_client: mqtt_client instance
        :param logger: logger instance from the parent. a child will be spawned
        """

        AService.__init__(self, config, mqtt_client, __name__, logger)
        self._address = self._config["address"]
        self._port = self._config["port"]
        self._username = self._config["username"]
        self._password = self._config["password"]
        self._from = self._config["from"]
        if isinstance(self._config["to"], str):
            self._to = [self._config["to"]]
        else:
            self._to = self._config["to"]

    def _start(self):
        if not self._test_connection():
            self._logger.error("EmailService._start - connection test failed")
            raise RuntimeError("EmailService._start - connection test failed")

    def _stop(self):
        pass

    def _test_connection(self):
        try:
            server = smtplib.SMTP_SSL(host=self._address, port=self._port)
            server.set_debuglevel(0)
            server.login(self._username, self._password)
            server.noop()
            server.quit()
            return True
        except smtplib.SMTPException as exception:
            self._logger.error("EmailService._test_connection - failed: {}.".format(exception))
        return False

    def _render_message(self, messages):
        body = "received {} messages since last update.\n".format(len(messages))
        body += "\nMessages:\n"
        for entry in messages:
            timestamp, topic, message = entry
            timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            body += "  {}; {}; '{}'\n".format(timestamp, topic, message)
        body += "EOF\n"
        return body

    def _send_message(self, subject, message):
        self._logger.debug("EmailService._send_message")
        msg = MIMEText(message)
        msg['To'] = ', '.join(self._to)
        msg['From'] = self._from
        msg['Subject'] = subject

        try:
            server = smtplib.SMTP_SSL(host=self._address, port=self._port)
            server.set_debuglevel(0)
            server.login(self._username, self._password)
            server.send_message(msg)
        except smtplib.SMTPException as exception:
            self._logger.error("EmailService._send_message - failed: {}.".format(exception))
            raise
        finally:
            server.quit()
