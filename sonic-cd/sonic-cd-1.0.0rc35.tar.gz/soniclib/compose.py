# -*- coding: utf-8 -*-
import glob
import json
import logging
import os
import shutil
import validators
from string import Template

import yaml
from dateutil.parser import parse

from soniclib import config, util
from soniclib.config import SONIC_PATH
from soniclib.context import Context
from soniclib.exceptions import NonZeroExitCodeException
from soniclib.logutils import LogPipe

with_pull = False
log_level = logging.INFO
task_config = {
    'shm_size': config.get("shm_size") or "512m",
    'mem_limit': config.get("mem_limit") or "2048m"
}


def run(name, compose_model, task_index=0):
    util.ensure_path(SONIC_PATH)
    file_name = SONIC_PATH + "sonic-" + name + str(task_index) + ".yaml"

    compose_template = Template(yaml.dump(compose_model, default_flow_style=False, indent=4))
    context = Context()
    context.set("sonic_task", name)
    with open(file_name, 'w') as compose_file:
        compose_file.write(compose_template.safe_substitute(context))

    logging.debug("Generated model:\n%s" % yaml.dump(compose_model))
    main_container_name = get_main_container_name(compose_model, name, task_index)
    main_image_name = get_main_image_name(compose_model, main_container_name)
    main_image_command = get_main_image_command(compose_model, main_container_name)
    monochrome_option = "--no-color" if config.get(config.Keys.monochrome) else ""
    compose_up_command = get_docker_compose_cmd(file_name) + \
        " up %s --abort-on-container-exit " % monochrome_option \
        + ("--exit-code-from " + main_container_name if main_container_name else "")
    print_banner([
        "%s (%s)" % (str.upper(name), task_index),
        "\t- main image: %s" % main_image_name,
        "\t- main command: %s" % main_image_command,
        "\t- compose file: %s" % file_name,
    ])
    do_print_command = logging.getLogger().level == logging.DEBUG
    if util.system_uses_vagrant():
        util.message("Cygwin/Windows detected, using a Vagrant box for docker-compose execution")
        if with_pull:
            vagrant_command = "cd /sonic && " + get_docker_compose_cmd(file_name) + " pull --ignore-pull-failures"
            with LogPipe(log_level) as log_pipe:
                util.run_in_box(vagrant_command, out=log_pipe)
        vagrant_command = "cd /sonic && " + compose_up_command
        with LogPipe(logging.getLogger().level) as log_pipe:
            exit_code, ignored_stdout = util.run_in_box(vagrant_command, out=log_pipe, print_command=do_print_command)
    else:
        if with_pull:
            with LogPipe(log_level) as log_pipe:
                util.run(get_docker_compose_cmd(file_name) + " pull --ignore-pull-failures", out=log_pipe,
                         print_command=do_print_command)
        try:
            with LogPipe(log_level) as log_pipe:
                exit_code, ignored_stdout = util.run(
                    compose_up_command,
                    print_command=do_print_command,
                    print_exit_code=False,
                    out=log_pipe
                )
            try:
                if exit_code == 0 and not is_stopped_by(main_container_name, compose_model, file_name):
                    logging.info("Not stopped by %s, aborting..." % main_container_name)
                    exit_code = 9
            except Exception as e:
                logging.warning("Unable to verify stop order: %s" % str(e))
        finally:
            take_down(file_name)
    if exit_code != 0:
        raise NonZeroExitCodeException(
            '%s step %s failed with exit code %s, aborting run' % (name, str(task_index), str(exit_code)))


def is_stopped_by(container_name, compose_model, file_name):
    if not container_name or not compose_model["services"] or len(compose_model["services"]) <= 1:
        return True

    stop_times = dict()
    for service, definition in compose_model["services"].items():
        ignored_exit_code, container_id = util.run(get_docker_compose_cmd(file_name) + " ps -q %s" % service,
                                                   print_command=False)
        ignored_exit_code, inspect_str = util.run("docker inspect %s" % container_id, print_command=False)
        inspect = json.loads(inspect_str)
        stop_times[service] = parse(inspect[0]["State"]["FinishedAt"])
        logging.info("%s finished at %s" % (service, stop_times[service]))

        in_stop_order = sorted(stop_times.items(), key=lambda p: (p[1], p[0] != container_name))
    return in_stop_order[0][0] == container_name


def get_docker_compose_cmd(file_name):
    project_name = None
    util.ensure_path(config.SONIC_PATH)
    if os.path.isfile(config.SONIC_PATH + "docker_project_name"):
        with open(config.SONIC_PATH + "docker_project_name", 'r') as f:
            project_name = f.read().strip()
    if not project_name:
        project_name = "sonic%s" % util.generate_id()
        with open(config.SONIC_PATH + "docker_project_name", 'w') as f:
            f.write(project_name)

    return "docker-compose --project-name %s --file %s " % (project_name, file_name)


def take_down(file_name):
    logging.debug("Cleaning up...")
    util.run(get_docker_compose_cmd(file_name) + " down -v", print_command=logging.getLogger().level == logging.DEBUG)
    with open(file_name, 'r') as compose_file:
        model = yaml.load(compose_file)
        gateway = model["networks"]["default"]["ipam"]["config"][0]["gateway"]
        if gateway:
            config.return_gateway(gateway)


def cleanup():
    if os.path.isdir(SONIC_PATH):
        logging.info("Taking down all docker compose setups")
        for file_name in glob.glob(SONIC_PATH + "sonic-*.yaml"):
            take_down(file_name)
        logging.info("Removing %s" % SONIC_PATH)
        shutil.rmtree(SONIC_PATH)


def create_model(name, task, task_index=0):
    logging.debug("name: %s, task_index: %s, task: %s" % (name, task_index, task))
    compose_model = dict()
    compose_model["version"] = "2.1"
    if isinstance(task, str):
        service = dict()
        task_parts = task.split(" ")
        service["user"] = "root"
        service["working_dir"] = "/workdir/"

        if task_parts[0] is not None:
            if task_parts[0].startswith("${component}"):
                pass  # the component itself is assumed to be a Docker image
            elif task_parts[0].startswith("$"):
                service["image"] = task_config.get("default_image") or config.get("default_image", "docker.io/alpine")
            elif "/" in task_parts[0]:
                image_parts = task_parts[0].split("/")
                if validators.domain(image_parts[0]):
                    service["image"] = task_parts[0]
                else:
                    service["image"] = "%s/%s" % (config.get_registry(), task_parts[0])
            else:
                service["image"] = "%s/%s" % (config.get_registry(), task_parts[0])

        if len(task_parts) > 1:
            service["command"] = " ".join(task_parts[1:])
        service["volumes"] = [
            "${workdir}:/workdir",
            "/var/run/docker.sock:/var/run/docker.sock",
            "${user_home}/.docker/config.json:/root/.docker/config.json:ro",
            "${user_home}/.aws:/root/.aws:ro",
            "${user_home}/.aws/cli:/root/.aws/cli",
            "${user_home}/.ssh:/root/.ssh:ro",
            "${user_home}/.gitconfig:/root/.gitconfig:ro",
        ]
        if util.get_maven_cache_location() is not None:
            service["volumes"].append("${maven_cache}:/var/cache/maven")
        if config.get(config.Keys.additional_volumes):
            service["volumes"].extend(config.get(config.Keys.additional_volumes))
        service['shm_size'] = task_config.get("shm_size") or "512m"
        service['mem_limit'] = task_config.get("mem_limit") or "2048m"

        environment = {
            "SONIC_TASK": "${sonic_task}",
            "ZONE": "${zone}",
            "SITE": "${site}",
            "SOLUTION": "${solution}",
            "ENVIRONMENT": "${environment}",
            "FLAVOUR": "${flavour}",
            "COMPONENT": "${component}",
            "SHORTNAME": "${shortname}",
            "VERSION": "${version}",
            "DOMAIN": "${domain}",
            "SSH_AUTH_SOCK": "/tmp/ssh_auth_sock"
        }
        if "http_proxy" in os.environ:
            environment["http_proxy"] = os.environ["http_proxy"]
        if "https_proxy" in os.environ:
            environment["https_proxy"] = os.environ["https_proxy"]
        if "no_proxy" in os.environ:
            environment["no_proxy"] = os.environ["no_proxy"]

        environment.update(get_aws_specific_environment_variables())
        
        service["environment"] = environment
        compose_model["services"] = {generate_main_container_name(name, task_index): service}
    else:
        services, named_volumes = util.format_model(task)
        compose_model["services"] = services
        if named_volumes:
            compose_model["volumes"] = named_volumes
    networks = config.get_networks()
    if networks:
        compose_model["networks"] = networks
    return compose_model


def get_main_container_name(compose_model, task_name, index):
    if "main" in compose_model["services"]:
        return "main"
    elif generate_main_container_name(task_name, index) in compose_model["services"]:
        return generate_main_container_name(task_name, index)


def generate_main_container_name(task_name, index):
    return "%ser%s" % (task_name, index) if not task_name[-1] == 'e' else "%sr%s" % (task_name, index)


def get_main_image_name(compose_model, main_container_name):
    return compose_model['services'][main_container_name]['image']


def get_main_image_command(compose_model, main_container_name):
    if 'command' in compose_model['services'][main_container_name]:
        return compose_model['services'][main_container_name]['command']
    else:
        return "<default image command>"


def get_aws_specific_environment_variables():
    environment = {}
    if "AWS_CONTAINER_CREDENTIALS_RELATIVE_URI" in os.environ:
        environment["AWS_CONTAINER_CREDENTIALS_RELATIVE_URI"] = os.environ["AWS_CONTAINER_CREDENTIALS_RELATIVE_URI"]
    return environment


def print_banner(task_message):
    max_line_length = len(max(task_message, key=len))
    separator_line = "".ljust(max_line_length, '-')
    debug = log_level is logging.DEBUG
    util.message(separator_line, debug)
    util.message("", debug)
    util.message(task_message[0], debug)
    util.message("", debug)
    util.message(task_message[1], debug)
    util.message(task_message[2], debug)
    util.message(task_message[3], debug)
    util.message("", debug)
    util.message(separator_line, debug)
