# -*- coding: utf-8 -*-
import logging
import os
import tempfile
import errno
import yaml

from soniclib import util
from soniclib.filelock import FileLock

__config = None

SONIC_PATH = ".sonic/"
DOCKER_CONFIG_FILE = util.get_user_home() + '/.docker/config.json'

USER_CONFIG_DIR = util.get_user_home() + '/.sonic'

CONFIG_DIRS = [
    '/etc/sonic',
    USER_CONFIG_DIR
]
CONFIG_FILE_NAME = "config.yml"

TEMP_DIR = '/tmp' if util.host_is_mac() else tempfile.gettempdir()
GATEWAYS_LOCK_DIR = TEMP_DIR + os.sep + 'sonic-gateways'


class Keys:
    registry = "registry"
    networks = "networks"
    use_vagrant = "use_vagrant"
    use_global_vagrant_box = "use_global_vagrant_box"
    current_project = "current_project"
    monochrome = "monochrome"
    additional_volumes = "additional_volumes"


def load():
    global __config
    if __config is None:
        __config = {}
        for config_dir in CONFIG_DIRS:
            config = util.load_yaml(os.path.join(config_dir, CONFIG_FILE_NAME))
            if config:
                __config.update(config)
        logging.debug("Loaded config:\n%s" % yaml.dump(__config))
    return __config


def clear():
    global __config
    __config = None


def get(key, default_value=None):
    sonic_conf = load()
    return sonic_conf.get(key, default_value)


def userconfig_update(dictionary):
    user_conf_file = os.path.join(USER_CONFIG_DIR, CONFIG_FILE_NAME)
    if not os.path.exists(USER_CONFIG_DIR):
        os.makedirs(USER_CONFIG_DIR)
    user_conf = util.load_yaml(user_conf_file) or {}
    user_conf.update(dictionary)
    with open(user_conf_file, "w") as user_config_file:
        yaml.dump(user_conf, user_config_file, default_flow_style=False, indent=4)


def get_registry():
    sonic_conf = load()
    if Keys.registry in sonic_conf:
        return sonic_conf[Keys.registry]
    else:
        if not util.in_unittest():
            util.message(
                "Attention: with no registry configured in %s, sonic will try to use registry information from %s" % (
                    ", ".join(CONFIG_DIRS), DOCKER_CONFIG_FILE))
        registry = None
        docker_conf = util.load_json(DOCKER_CONFIG_FILE)
        if docker_conf and "auths" in docker_conf:
            registry = list(docker_conf["auths"].keys())[0]
        if registry is None:
            raise Exception("No registry found in %s, or %s" % (", ".join(CONFIG_DIRS), DOCKER_CONFIG_FILE))
        else:
            return registry


def get_networks():
    sonic_conf = load()
    return sonic_conf[Keys.networks] if Keys.networks in sonic_conf else get_default_networks()


def get_default_networks():
    gateway = get_available_gateway()
    return {
        "default": {
            "driver": "bridge",
            "driver_opts": {
                "com.docker.network.driver.mtu": "1400"
            },
            "ipam": {
                "driver": "default",
                "config": [{
                    "subnet": gateway + "/24",
                    "gateway": gateway
                }],
            }
        }
    }


def get_available_gateway():
    lock_path = tempfile.gettempdir() + os.sep + 'sonic-get_available_gateway.lock'
    util.ensure_path(GATEWAYS_LOCK_DIR)
    lock = FileLock(lock_path, timeout=10)
    with lock:
        for x in range(70, 255):
            gateway = "192.168.%d.1" % x
            try:
                util.create_file(GATEWAYS_LOCK_DIR + os.sep + gateway)
                logging.debug("Returning available gateway %s" % gateway)
                return gateway
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise


def return_gateway(gateway):
    lock_path = tempfile.gettempdir() + os.sep + 'sonic-get_available_gateway.lock'
    util.ensure_path(GATEWAYS_LOCK_DIR)
    lock = FileLock(lock_path, timeout=10)
    with lock:
        try:
            os.remove(GATEWAYS_LOCK_DIR + os.sep + gateway)
            logging.debug("Returned gateway %s" % gateway)
        except OSError as e:
            logging.error("Error: %s - %s." % (e.filename, e.strerror))


def log():
    load()
    msg = ""
    msg = msg + "Reading from:" + "\n"
    msg = msg + "-------------" + "\n"
    for dir in CONFIG_DIRS:
        config_file = os.path.join(dir, CONFIG_FILE_NAME)
        msg = msg + " - %s : %s" % (config_file, os.path.isfile(config_file)) + "\n"
    msg = msg + "" + "\n"
    msg = msg + "Current config:" + "\n"
    msg = msg + "---------------" + "\n"
    msg = msg + yaml.dump(__config, default_flow_style=False, indent=4)
    logging.info(msg)
