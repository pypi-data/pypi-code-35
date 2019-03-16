import os
import simplejson as json
import logging


class ConfigManager(object):
    """
    Config loader class
    """
    _environment = 'develop'
    config = {}

    def load(self, path, environment):
        """
        Loads the specified filename into the configuration manager, loads default config if not available
        :param path: the path to the configuration files
        :param environment: the environment in which the configuration files are stored
        """
        self._environment = environment
        filename = '{}/{}.json'.format(path, environment)

        with open(filename) as data:
            self.config = json.load(data)
        logging.info('Loaded configuration from file [{}]'.format(filename))

    def get(self, parameter):
        """
        Retrieve the specified parameter from either environment (lambdas) or config
        :param parameter: The parameter name
        :return: The configuration item
        :except: throws ConfigException if the parameter doesn't exist
        """
        value = os.environ.get(parameter, None)

        if not value:
            value = self.config.get(parameter, None)

        if not value:
            raise ConfigException('Failed to read configuration item [{}]'.format(parameter))

        return value

    @property
    def environment(self):
        return self._environment


class ConfigException(StandardError):
    pass
