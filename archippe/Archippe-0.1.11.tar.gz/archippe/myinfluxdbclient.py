from influxdb import InfluxDBClient
from pelops.logging.mylogger import get_child
import datetime


class MyInfluxDBClient:
    """
    Wrapper for influxdb.MyInfluxDBClient. Takes care initializing and writing of single datapoints to the db.

    In the configuration file you can choose to either provide an credentials file ("credentials-file") or to add
    the credentials directly ("influx-user", "influx-password").

    influx:
        influx-address: localhost
        influx-port: 8086
        credentials-file: ~/credentials.yaml
        database: archippe_test
        log-level: DEBUG  # log level to be used by logger

    credentials-file file:
    influx:
        influx-password: secret
        influx-username: user
    """

    client = None  # instance of InflucDBClient.influxdb
    _influxdb_username = None
    _influxdb_password = None
    _influxdb_address = None
    _influxdb_port = None
    _influxdb_database = None

    _config = None  # config yaml
    _logger = None  # logger instance

    def __init__(self, config, logger):
        """
        Constructor

        :param config: yaml structure
        :param logger: logger instance - a child with name __name__ will be spawned.
        """
        self._config = config
        self._logger = get_child(logger, __name__, config)
        self._logger.info("MyInfluxDBClient.__init__ - creating instance.")
        self._logger.debug("MyInfluxDBClient.__init__ - config: {}".format(self._config))

        self._influxdb_address = str(self._config["influx-address"])
        self._influxdb_port = int(self._config["influx-port"])
        self._influxdb_database = str(self._config["database"])
        self._influxdb_password = str(self._config["influx-password"])
        self._influxdb_username = str(self._config["influx-user"])

        self.client = InfluxDBClient(host=self._influxdb_address, port=self._influxdb_port,
                                       username=self._influxdb_username, password=self._influxdb_password,
                                       database=self._influxdb_database)

    def _get_json_entry(self, measurement, value, timestamp):
        """
        Generate a valid json entry for the influxdb.write_points method

        :param measurement: name of measurement
        :param value: value to be stored
        :param timestamp: string in the format "2009-11-10T23:00:00.0Z".
        :return: dict - json structure
        """
        result = {
                "measurement": MyInfluxDBClient.escape_name(measurement),
                "tags": {},
                "time": timestamp,
                "fields": {
                    "value": value
                }
            }
        return result

    @staticmethod
    def _to_influx_timestamp(ht, epoch=datetime.datetime(1970, 1, 1)):
        """datatime cannot convert a datetimestring with nanoseconds"""
        dt = datetime.datetime.strptime(ht[:-4], '%Y-%m-%dT%H:%M:%S.%f')
        nanoseconds = int(ht[-4:-1])
        td = dt - epoch
        result = (td.microseconds + (td.seconds + td.days * 86400) * 10 ** 6)
        result = result * 10 ** 3 + nanoseconds
        return result

    def write_point(self, measurement, value, timestamp=None):
        """
        Write a single measurement value to the database (wrapper for influxdb.write_points method).

        :param measurement: name of measurement
        :param value: value to be stored
        :param timestamp: string in the format "2009-11-10T23:00:00.0Z". if None is provided, the current time is used.
        """
        if timestamp is None:
            timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")  # "2009-11-10T23:00:00.0Z"

        json_body = [
            self._get_json_entry(measurement, value, timestamp)
        ]
        self._logger.info("Write a point: (measurement: {}, timestamp: {}, value: {})".
                          format(measurement, timestamp, value))
        self._logger.debug("Json: {}.".format(json_body))
        self.client.write_points(json_body)

    def write_points(self, measurement, entries):
        """
        Write a list of entries (timestamp, value) into the measurement of the database. A timestamp must be a string
        with the format "2009-11-10T23:00:00.0Z".

        :param measurement: name of measurement
        :param entries: list of (value, timestamp) tuples
        """
        json_body = []
        for entry in entries:
            value, timestamp = entry
            json_body.append(self._get_json_entry(measurement, value, timestamp))
        self._logger.info("Write {} points to measurement {}.".
                          format(len(entries), measurement))
        self._logger.debug("value/timestamp tuples: {}".format(entries))
        self._logger.debug("Json: {}.".format(json_body))
        self.client.write_points(json_body)

    @staticmethod
    def escape_name(name):
        # https://stackoverflow.com/questions/47273602/how-to-insert-store-a-string-value-in-influxdb-measurement
        name = name.replace(" ", "\ ")
        name = name.replace(",", "\,")
        return name
