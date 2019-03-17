import logging
import os
from functools import wraps

import click
import jwt
from missinglink.crypto import Asymmetric

from .configuration import get_active_config, load_config

logger = logging.getLogger(__name__)


def config_params(fn):
    @wraps(fn)
    @click.option('token', '--token', '--ml-token', help='Resource identifying token generated by MissingLink')
    @click.option('ws_server', '--ml-server', '--ws', help='Resource identifying token generated by MissingLink')
    @click.option('--ml-config-prefix', default=None, help='')
    @click.option('--ml-config-file', help='')
    @click.option('--capacity', type=int, help='The number of maximum concurrent GPUs jobs that can run on this host. Applies to local-grid local-grid servers only. The capacity must be a divisor of the GPU count')
    @click.option('--debug', is_flag=True, help='run in debug mode')
    @click.option('backend_base_url', '--ml-backend', '--backend', default='https://missinglinkai.appspot.com/_ah/api/missinglink/v1', help='backend base url')
    @click.option('--ssh-private-key', help='Path to the private key to be used when working with source control.')
    @click.option('--env', type=(str, str), multiple=True, help='Additional environment variables to be set on containers started by the resource manager')
    @click.option('--hostname', type=str, help='Hostname to use for this host. The hostname is passed as environment variable (ML_SERVER_NAME)')
    @click.option('--mount', type=(str, str), multiple=True, help='Additional volume mappings to be performed on containers started by the resource manager.')
    @click.option('--docker-auth', type=(str, str, str), multiple=True, help='Docker HOST USER PASS (in this order!) to be used before pulling new images. ECR are still authenticated automatically')
    @click.option('--cache-path', help='Path to persistent cache')
    def decorated(**kwargs):
        load_config()
        ConfigBuilder.update(kwargs)
        return fn(**kwargs)

    return decorated


class ConfigBuilder(object):
    @classmethod
    def update(cls, kwargs):
        new_configuration = cls.build_config(kwargs)
        updated_config = cls(**new_configuration)  # used for configuration migration
        updated_config.parse_and_save()
        return updated_config

    def __init__(self, **kwargs):
        self.active_config = kwargs.pop('active_config', get_active_config())
        self.kwargs = kwargs

    @classmethod
    def _ensure_b64(cls, config_data_str):
        if 'access_token' in config_data_str:
            return Asymmetric.bytes_to_b64str(config_data_str)

        return config_data_str

    @classmethod
    def save_ml_config(cls, config, config_prefix, config_data):
        filename = 'missinglink.cfg'
        if config_prefix is not None and len(config_prefix) > 0:
            filename = f"{config_prefix}-{filename}"

        config_data = cls._ensure_b64(config_data)
        config.general.ml_data = config_data
        config.general.ml_path = filename

    @classmethod
    def populate_ssh_key(cls, active_config, ssh_key_data):
        cipher = Asymmetric.create_from(Asymmetric.ensure_bytes(ssh_key_data))
        active_config.general.default_public_key = cipher.bytes_to_b64str(cipher.export_public_key_bytes())
        active_config.general.default_private_key = cipher.bytes_to_b64str(cipher.export_private_key_bytes('PEM'))
        # todo: load old keys

    @classmethod
    def build_config(cls, kwargs):
        new_config = {
            'token': kwargs.pop('token', None), 'debug': kwargs.pop('debug', None),
            'ws_server': kwargs.pop('ws_server', None),
            'capacity': kwargs.pop('capacity', None),
            'ssh_private_key': kwargs.pop('ssh_private_key', None),
            'ml_config_file': kwargs.pop('ml_config_file', None),
            'ml_config_prefix': kwargs.pop('ml_config_prefix', None),
            'backend_base_url': kwargs.pop('backend_base_url', None),
            'hostname': kwargs.pop('hostname', None),
            'env': {t[0]: t[1] for t in kwargs.pop('env', [])},
            'mount': {t[0]: t[1] for t in kwargs.pop('mount', [])},
            'cache_path': kwargs.pop('cache_path', None),
            'docker_auth': {t[0]: {'user': t[1], 'pass': t[2]} for t in kwargs.pop('docker_auth', [])}}
        return {k: v for k, v in new_config.items() if v}

    def _get_hostname(self):
        from ..controllers.docker.docker_wrapper import DockerWrapper
        try:
            info = DockerWrapper.get().raw_status()
            self.active_config.general.hostname = info['Name']
        except Exception as ex:
            import socket
            hostname = socket.gethostname()
            logger.warning('Failed to obtain hostname from docker %s failing back to %s', str(ex), hostname)
            self.active_config.general.hostname = hostname

    def _set_slots(self, gpus):
        capacity = self.kwargs.pop('capacity', self.active_config.general.get('capacity', 1))

        if gpus is None:
            self.active_config.general.slots = [None]  # None means no gpus. when/if we have CPU capacity CPU ids will be stored here
            self.active_config.general.capacity = 1
            return

        gpu_count = len(gpus)
        capacity_reminder = gpu_count % capacity
        if capacity_reminder != 0:
            logger.error(f'The specified capacity {capacity} can not be fulfilled by the number of gpus found {gpu_count} ')
            self.active_config.general.slots = [None]
            self.active_config.general.capacity = 1
            return

        slot_size = gpu_count // capacity
        slots = [gpus[i:i + slot_size] for i in range(0, gpu_count, slot_size)]
        self.active_config.general.slots = slots
        self.active_config.general.capacity = capacity
        logger.debug('Allocated slots: %s', slots)

    def _has_gpu(self):
        from ..controllers.docker.docker_wrapper import DockerWrapper
        gpus = DockerWrapper.get().has_nvidia()
        self.active_config.general.gpu = gpus is not None
        self._set_slots(gpus)

    def _conf_hostname(self):
        provided_hostname = self.kwargs.pop('hostname', None)
        if provided_hostname:
            self.active_config.general.hostname = provided_hostname
        else:
            if self.active_config.general.get('hostname') is None:
                self._get_hostname()

        logger.debug('Hostname: %s', self.active_config.general.hostname)

    def _conf_ws_server(self):
        ws_server = self.kwargs.pop('ws_server', None)
        if ws_server is not None:
            self.active_config.general.ws_server = ws_server
            logger.debug('Missing Link Server is set to %s', ws_server)

    def _conf_backend_base_url(self):
        backend_base_url = self.kwargs.pop('backend_base_url', None)
        if backend_base_url:
            self.active_config.general.backend_base_url = backend_base_url
            logger.debug('Missing Link backend_base_url is set to %s', backend_base_url)

    def _conf_ml_token(self):
        ml_token = self.kwargs.pop('token', None)

        if ml_token is not None:
            tok = jwt.decode(ml_token, verify=False)
            sid = tok.get("uid")
            self.active_config.general.cluster_id = sid
            self.active_config.general.jwt = ml_token
            self.active_config.general.save()
            logger.debug('Missing Link Token is set. Resource Id: %s', sid)

    def _conf_ssh_key(self):
        ssh_private_key = self.kwargs.pop('ssh_private_key', None)
        if ssh_private_key is not None:
            self.populate_ssh_key(self.active_config, ssh_private_key)
            logger.debug('SSH key is set')

    def _conf_ml_creds(self):
        ml_config_prefix = self.kwargs.pop('ml_config_prefix', None)
        ml_config_file = self.kwargs.pop('ml_config_file', None)
        if ml_config_file is not None:
            if ml_config_prefix == str(None):
                ml_config_prefix = None

            self.active_config.general.ml_prefix = ml_config_prefix
            self.save_ml_config(self.active_config, config_prefix=ml_config_prefix, config_data=ml_config_file)
            logger.debug('Credentials set')

    def _conf_cache(self):
        self.active_config.general.config_volume = os.environ.get('ML_CONFIG_VOLUME', 'ml_config_volume')
        path = self.kwargs.pop('cache_path', None)
        if path:
            self.active_config.general.cache_path = path

    def _conf_env(self):
        env = self.kwargs.pop('env', {})
        if env:
            self.active_config.general.env = env
            logger.debug('env is set: %s items', len(env))

    def _conf_mounts(self):
        mounts = self.kwargs.pop('mount', {})
        if mounts:
            self.active_config.general.mount = mounts
            logger.debug('mounts is set: %s items', len(mounts))

    def _conf_docker_auths(self):
        docker_auths = self.kwargs.pop('docker_auth', {})
        if docker_auths:
            self.active_config.general.docker_auth = docker_auths
            logger.debug('docker_auths is set: %s items', len(docker_auths))

    def _conf_debug(self):
        debug = self.kwargs.pop('debug', os.environ.get('MLADMIN_DEBUG'))
        if debug is not None:
            self.active_config.general.debug = debug
            logger.debug('debug? %s', debug)

    def parse_and_save(self):
        self._conf_debug()
        self._conf_hostname()
        self._conf_ws_server()
        self._conf_backend_base_url()
        self._conf_ml_token()
        self._conf_ssh_key()
        self._conf_ml_creds()
        self._conf_env()
        self._conf_mounts()
        self._conf_docker_auths()
        self._conf_cache()
        self._has_gpu()
        self.active_config.general.save()
        logger.debug(f"{self.active_config.config_path} Saved")
