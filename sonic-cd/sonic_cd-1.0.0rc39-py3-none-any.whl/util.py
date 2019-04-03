# -*- coding: utf-8 -*-

import errno
import inspect
import json
import logging
import logging.config
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

import yaml

from soniclib import config, logutils
from soniclib.context import Context

try:
    import grp
except ImportError:
    logging.info("The grp module is not available on this platform")

MESSAGE_PREFIX = "SONIC:"
MC_MESSAGE_FORMAT = MESSAGE_PREFIX + " %s"
COLOR_MESSAGE_FORMAT = "\033[0;34m" + MESSAGE_PREFIX + "\033[0;0m %s"
COMMAND_PREFIX = "SONIC>"
MC_COMMAND_FORMAT = COMMAND_PREFIX + " %s"
COLOR_COMMAND_FORMAT = "\033[0;34m" + COMMAND_PREFIX + "\033[0;0m %s"

DOMAIN_PARTS = [
    'zone',
    'site',
    'solution',
    'environment'
]

PLACEHOLDERS = ['workdir',
                'maven_cache',
                'maven_release_repository',
                'npm_cache',
                'component',
                'semantic_version',
                'version',
                'shortname',
                'domain',
                'user_home',
                'flavour'
                ] + DOMAIN_PARTS


def get_user_home():
    return os.path.expanduser("~")


def get_docker_user_home():
    return "/home/sonic" if system_uses_vagrant() else os.path.expanduser("~")


def ensure_path(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def create_file(path):
    if host_is_mac():
        if os.path.exists(path):
            raise OSError(errno.EEXIST, 'File exists', path)
        open(path, 'w').close()
    else:
        os.mknod(path)


def load_yaml(file_name, file_mode="r"):
    logging.debug("Loading %s" % file_name)
    file = get_file(file_name)
    if file:
        with open(file.name, file_mode) as yaml_file:
            return yaml.load(yaml_file)


def load_json(file_name, file_mode="r"):
    file = get_file(file_name)
    if file:
        with open(file.name, file_mode) as json_file:
            return json.load(json_file)


def get_component():
    return os.getcwd().split('/')[-1]


def format_image(image):
    if "/" not in image:
        image = "%s/%s" % (config.get_registry(), image)
    return image


def get_maven_cache_location():
    return "/var/opt/maven/repository" if system_uses_vagrant() else get_local_maven_repository()


def get_npm_cache_location():
    return get_docker_user_home() + "/.npm"


def get_docker_daemon_json_location():
    prefix = get_docker_user_home() + "/.docker/" if host_is_mac() else "/etc/docker/"
    return prefix + "daemon.json"


# this function is just here because I couldn't figure out how to mock os.getuid() and os.environ in test_util.test_format_model
def get_user_id():
    return os.getuid()


def get_docker_group_id():
    return grp.getgrnam('staff').gr_gid if host_is_mac() else grp.getgrnam('docker').gr_gid


def replacement_value_for(key):
    context = Context()
    if hasattr(context, key):
        return getattr(context, key)
    elif key in os.environ and len(os.environ[key]) > 0:
        return os.environ[key]
    else:
        return get_fallback_replacement_for(key)


def get_fallback_replacement_for(key, sonic_model=None):
    fallback = 'sonic' if key in DOMAIN_PARTS else {
        'workdir': '..',
        'maven_cache': get_maven_cache_location(),
        'maven_release_repository': get_local_maven_repository(),
        'npm_cache': get_npm_cache_location(),
        'component': get_project_name(),
        'shortname': get_shortname(sonic_model),
        'user_home': get_docker_user_home(),
        'semantic_version': '0-SNAPSHOT',
        'version': '0-SNAPSHOT',
        'domain': get_domain()
    }.get(key)
    return fallback


def get_domain():
    return "%s.%s.%s.%s.%s" % (
        replacement_value_for("environment"),
        replacement_value_for("solution"),
        replacement_value_for("site"),
        replacement_value_for("zone"),
        config.get("domain") or "UNCONFIGURED_DOMAIN"
    )


def generate_shortname():
    directory_name = get_project_name()
    joined_directory_name_initials = ''.join([word[0] for word in directory_name.split('-')])
    return joined_directory_name_initials[:8] if len(directory_name) > 8 else directory_name


def get_project_name():
    directory_name = os.getcwd().split('/')[-1]
    return directory_name


def get_shortname(sonic_model):
    if sonic_model:
        if "shortname" in sonic_model:
            return sonic_model.get("shortname")
        if "shortName" in sonic_model:
            return sonic_model.get("shortName")

    return generate_shortname()


def format_model(task_model):
    named_volumes = dict()
    for service in task_model:
        if 'volumes' in task_model[service]:
            for index, volume in enumerate(task_model[service]['volumes']):
                volume_name = volume.split(':')[0]
                if all(st not in volume_name for st in ['/', '..', '$']) and volume_name not in named_volumes:
                    named_volumes[volume_name] = dict()
                task_model[service]['volumes'][index] = volume

    return task_model, named_volumes


def is_older_than_five_minutes_or_missing(file_name):
    if not os.path.exists(file_name):
        return True
    m_time = os.path.getmtime(file_name)
    return time.time() - m_time > 5 * 60


def get_message_format():
    return MC_MESSAGE_FORMAT if config.get(config.Keys.monochrome) else COLOR_MESSAGE_FORMAT


def get_command_format():
    return MC_COMMAND_FORMAT if config.get(config.Keys.monochrome) else COLOR_COMMAND_FORMAT


def message(_message, debug=False):
    if debug:
        logging.debug(get_message_format() % _message)
    else:
        logging.info(get_message_format() % _message)


def command(_command):
    logging.info(get_command_format() % _command)


def newline():
    print("")


def truncate(text):
    if len(text) > 220:
        return text[:217] + "..."
    else:
        return text


def run(args, quiet=False, print_exit_code=False, print_command=True, out=subprocess.PIPE, env=os.environ.copy()):
    if not isinstance(args, str):
        args = " ".join(args)

    if print_command:
        command(args)

    if quiet:
        out = open(os.devnull, 'wb')

    process = subprocess.Popen(args, shell=True, stdout=out, stderr=subprocess.STDOUT, env=env)
    process_stdout = process.communicate()[0]
    exit_code = process.returncode

    if print_exit_code:
        print(exit_code)

    return exit_code, process_stdout


def run_in_box(command, quiet=False, print_exit_code=False, print_command=True, out=subprocess.PIPE,
               env=os.environ.copy()):
    logging.debug("running in box: %s" % command)
    if use_global_vagrant_box():
        ssh_command = get_ssh_command_for_global_box()
        return run(ssh_command + " '%s'" % command, quiet, print_exit_code=print_exit_code, print_command=print_command,
                   out=out, env=env)
    else:
        return run("vagrant ssh -c '%s'" % command, quiet, print_exit_code, print_command, out, env)


def get_ssh_command_for_global_box():
    env = os.environ.copy()
    env["VAGRANT_CWD"] = get_vagrant_dir().replace("\\", "\\\\")
    exit_code, stdout = run("vagrant ssh-config", env=env, print_command=False)
    if exit_code > 0:
        raise Exception("vagrant ssh-config exited with non-0 exit code (%s): %s" % (str(exit_code), stdout))
    host_name = "127.0.0.1"
    port = 2240
    user = "sonic"
    identity_file = ""
    for line in stdout.split('\n'):
        # filter lines like these:
        # gems/2.4.4/gems/virtualbox-0.8.6/lib/virtualbox/com/ffi/util.rb:93: warning: key "io" is duplicated and overwritten on line 107"
        #
        if len(line) > 1 and "warning" not in line:  # just a newline isn't enough
            key, val = line.strip().split(' ')
            if key == "HostName":
                host_name = val
            if key == "Port":
                port = val
            if key == "User":
                user = val
            if key == "IdentityFile":
                identity_file = val
                if host_is_windows():
                    os.chmod(identity_file, 400)
            # 	identity_file = identity_file.replace('/', '\\\\')
    ssh_options = "-o 'UserKnownHostsFile=/dev/null' -o 'StrictHostKeyChecking=no' -o 'LogLevel=error'"
    ssh_command = "ssh %s -p %s -i %s %s@%s" % (ssh_options, port, identity_file, user, host_name)
    return ssh_command


def system_uses_vagrant():
    _system_uses_vagrant = config.get(config.Keys.use_vagrant, False) or host_is_windows()
    # logging.debug("system_uses_vagrant: %s" % _system_uses_vagrant)
    return _system_uses_vagrant


def host_is_linux():
    return re.match("Linux", platform.system())


def host_is_cygwin():
    _host_is_cygwin = re.match("CYGWIN_NT", platform.system()) is not None
    # logging.debug("_host_is_cygwin: %s" % _host_is_cygwin)
    return _host_is_cygwin


def host_is_windows():
    return re.match("Windows", platform.system()) is not None or host_is_cygwin()


def host_is_mac():
    return re.match("Darwin", platform.system(), re.IGNORECASE)


def get_file(path):
    try:
        return open(path)
    except IOError as exception:
        return None


def get_maven_settings_file():
    # User-level settings
    settings_file = get_file(os.path.expanduser("~") + '/.m2/settings.xml')
    # Fallback: use the system-wide settings
    if settings_file is None or not os.path.isfile(settings_file.name):
        settings_file = get_file(os.environ["M2_HOME"] + '/conf/settings.xml') if "M2_HOME" in os.environ else None
    return settings_file


def get_local_maven_repository():
    settings_file = get_maven_settings_file()
    if settings_file is None:
        return None
    import xml.etree.ElementTree as ET
    tree = ET.parse(settings_file)
    root = tree.getroot()
    local_repository_element = root.find(root.tag.replace('settings', 'localRepository'))
    if local_repository_element is not None:
        return local_repository_element.text
    else:
        return os.path.expanduser("~") + '/.m2/repository'


def file_age_seconds(the_file):
    mtime = os.path.getmtime(the_file.name)
    now = time.time()
    return round(now - mtime)


def use_global_vagrant_box():
    if config.Keys.use_global_vagrant_box in config.load():
        return bool(config.get(config.Keys.use_global_vagrant_box))
    if get_file("Vagrantfile"):
        return False
    return True


def modification_time(path):
    return os.path.getmtime(path) if os.path.isfile(path) else -1


def get_vagrant_dir():
    vagrant_dir = config.USER_CONFIG_DIR if use_global_vagrant_box() else os.getcwd()

    if host_is_cygwin():
        exit_code, cygwin_prefixed_vagrant_dir = run("cygpath.exe -am %s" % vagrant_dir, print_command=False)
        if exit_code > 0:
            raise Exception("cygpath.exe returned non-0 exit code (%s)" % str(exit_code))
        logging.debug("cygwin_prefixed_vagrant_dir=%s" % cygwin_prefixed_vagrant_dir)
        return cygwin_prefixed_vagrant_dir.strip()
    else:
        return vagrant_dir


def vagrant_up():
    current_dir = os.getcwd()
    if host_is_cygwin():
        exit_code, current_dir = run("cygpath.exe -am %s" % current_dir, print_command=False)
        if exit_code > 0:
            raise Exception("Failed executing cygpath.exe: %s" % current_dir)
        else:
            current_dir = current_dir.strip()
    conf = config.load()
    vagrant_dir = get_vagrant_dir()
    if use_global_vagrant_box():
        if config.Keys.current_project in conf and not conf[config.Keys.current_project] == current_dir:
            message("Reloading Vagrant box")
            vagrant_halt()
        pattern = '\s+config.vm.synced_folder\s"[\w\.\:/\-_]*",\s"/sonic",\sowner:\s"sonic",\sgroup:\s"sonic"'
        required_line = '        config.vm.synced_folder "%s", "/sonic", owner: "sonic", group: "sonic"' % current_dir
        logging.debug("required_line=%s" % required_line)
        replace_add(pattern, required_line, os.path.join(vagrant_dir, "Vagrantfile"), dryrun=False, print_message=False)
    env = os.environ.copy()
    env["VAGRANT_CWD"] = vagrant_dir
    rc, stdout = run('vagrant status | grep --quiet running', print_command=False, env=env)
    if rc != 0:
        exit_code, stdout = run("vagrant up", print_command=False, out=sys.stdout, env=env)
        # Clean out old containers to avoid container name conflicts
        message("Removing any old containers and networks")
        run("vagrant ssh -c 'docker ps -q -a | xargs docker rm 2>/dev/null'", print_command=False, out=sys.stdout,
            env=env)
        run("vagrant ssh -c 'docker network prune --force 2>/dev/null'", print_command=False, out=sys.stdout, env=env)
        config.userconfig_update({config.Keys.current_project: current_dir})
        return exit_code


def vagrant_halt():
    env = os.environ.copy()
    env["VAGRANT_CWD"] = get_vagrant_dir()
    exit_code, stdout = run("vagrant halt", print_command=False, out=sys.stdout, env=env)
    return exit_code


def store_as_json(dictionary, file_path, indent=2):
    temp_file = tempfile.NamedTemporaryFile()
    json.dump(dictionary, temp_file, indent=indent)
    temp_file.flush()
    shutil.copy(temp_file.name, file_path)
    temp_file.close()


def add_system_user(user_name, user_id, dryrun):
    message("Adding the %s user" % user_name)
    if host_is_mac():
        user_add_command = "sudo dscl . -create /Users/%s" % user_name
        command(user_add_command)
        ec_dscl = 0
        if not dryrun:
            ec_dscl = run(user_add_command, print_command=False)[0]
        user_add_command = "sudo dscl . -create /Users/%s UniqueID %s" % (user_name, user_id)
        command(user_add_command)
        if not dryrun:
            ec_dscl += run(user_add_command, print_command=False)[0]
        return 0 if dryrun else ec_dscl
    else:
        user_add_command = "useradd -u %s %s" % (user_id, user_name)
        command(user_add_command)
        return 0 if dryrun else run(user_add_command, print_command=False)[0]


def modify_group(group_name, group_id, dryrun):
    message("Modifying the %s group ID" % group_name)
    if host_is_mac():
        groupmod_command = "sudo dseditgroup -o edit -g %s %s" % (group_id, group_name)
        command(groupmod_command)
        return 0 if dryrun else run(groupmod_command, print_command=False)[0]
    else:
        groupmod_command = "groupmod --gid %s %s" % (group_id, group_name)
        command(groupmod_command)
        return 0 if dryrun else run(groupmod_command, print_command=False)[0]


def replace_add(pattern, required_line, file_path, dryrun=False, print_message=True):
    temp_file = tempfile.NamedTemporaryFile()
    if get_file(file_path):
        with open(file_path, "r") as input_file:
            for line in input_file.xreadlines():
                line = re.sub(pattern, required_line, line)
                temp_file.write(line)
            temp_file.flush()
            temp_file.seek(0)
    # if the required line didn't end up there by substitution, add it explicitly
    if required_line not in temp_file.read():
        temp_file.write(required_line)
    temp_file.flush()
    temp_file.seek(0)
    if print_message:
        message("Storing the following in %s:" % file_path)
        print(temp_file.read()[:-1])
    if not dryrun:
        temp_file.seek(0)
        shutil.copy(temp_file.name, file_path)
    temp_file.close()


def generate_id():
    return str(uuid.uuid4()).replace("-", "")


def setup_logging(debug):
    logging_ini_file_path = "%s/logging.ini" % config.USER_CONFIG_DIR
    logging_config_file = get_file(logging_ini_file_path)

    if logging_config_file:
        logging.info("Configuring logging from %s" % logging_config_file.name)
        logging.config.fileConfig(logging_config_file.name)
        root_logger = logging.getLogger()
        root_logger.addFilter(logutils.LogStashFilter(logging.INFO))
    else:
        logging.basicConfig(format='%(message)s')
        logging.info("%s not found, using default logging configuration" % logging_ini_file_path)

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Logging on debug level")
    else:
        logging.getLogger().setLevel(logging.INFO)


def get_platform_resources():
    resources = []
    if system_uses_vagrant():
        resources.append('resources/Vagrantfile')
    if re.match("CYGWIN_NT", platform.system()):
        resources.append('resources/cygwin/config.yml')
    else:
        resources.append('resources/config.yml')
    return resources


def init_config():
    base_path = os.path.dirname(__file__)
    config_folder = os.path.join(os.path.expanduser("~"), ".sonic")
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)
    for resource in get_platform_resources():
        file_name = os.path.basename(resource)
        from_path = os.path.join(base_path, resource)
        to_path = os.path.join(config_folder, file_name)
        if not os.path.isfile(to_path):
            logging.info("Copying config to %s" % to_path)
            shutil.copyfile(from_path, to_path)


def in_unittest():
    current_stack = inspect.stack()
    for stack_frame in current_stack:
        if "unittest" in stack_frame[1]:
            return True
    return False
