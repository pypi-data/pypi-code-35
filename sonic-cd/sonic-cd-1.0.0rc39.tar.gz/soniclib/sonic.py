# -*- coding: utf-8 -*-
import copy
import json
import logging
import os
import sys
import pkg_resources
import yaml

from soniclib import config, util, metrics, compose
from soniclib.context import Context

from soniclib.exceptions import NonZeroExitCodeException, PipeNotFoundException, SonicException


def get_sonic_profile():
    exit_code, ignore = util.run("aws configure --profile sonic list")
    return "sonic" if exit_code == 0 else None


def login_if_needed(forced=False, debug=False):
    user_home = "/home/sonic" if util.system_uses_vagrant() else util.get_user_home()
    login_needed = forced
    if util.system_uses_vagrant():
        if util.vagrant_up() > 0:
            raise Exception("Failed starting Vagrant box")
        if not forced:
            never_logged_in_condition = "[ ! -e $HOME/.docker/config.json ]"
            token_too_old_condition = "[ $(expr $(date +%s) - $(date +%s -r $HOME/.docker/config.json)) -ge 39600 ]"
            login_needed_condition = never_logged_in_condition + " || " + token_too_old_condition
            exit_code, ignored_stdout = util.run_in_box(login_needed_condition, print_command=debug)
            login_needed = exit_code == 0
        if login_needed:
            util.message("Authenticating against ECR")
            source_proxy_command = "[ -e /etc/profile.d/proxy.sh ] && source /etc/profile.d/proxy.sh || true"
            ecr_login_command = "eval $(/usr/local/bin/aws --profile sonic ecr get-login --no-include-email) 2>/dev/null"
            util.run_in_box(source_proxy_command + " && " + ecr_login_command, print_command=debug)
    else:
        docker_config_path = "%s/.docker/config.json" % user_home
        docker_config_file = util.get_file(docker_config_path)
        if not forced:
            login_needed = docker_config_file is None or os.path.getsize(
                docker_config_path) < 25 or util.file_age_seconds(docker_config_file) > 39600
        if login_needed:
            aws_profile = get_sonic_profile()
            util.run("eval $(aws %s ecr get-login --no-include-email) 2>/dev/null" % (
                " --profile %s " % aws_profile if aws_profile else ""))
        if docker_config_file is not None:
            os.chmod(docker_config_file.name, 640)  # make it readable for group


def init_context(sonic_model, context_args):
    util.ensure_path(config.SONIC_PATH)
    context = Context()
    context.clear()

    for key in util.PLACEHOLDERS:
        context.setdefault(key, util.get_fallback_replacement_for(key, sonic_model))

    context.update(context_args)
    context.save()


def args_to_dict(args):
    d = dict()
    if len(args) > 0:
        for pair in args:
            logging.debug("context pair: %s" % pair)
            kv = pair.split(":", 1)
            d[kv[0]] = kv[1]
    return d


def run(parser_result):
    try:
        if parser_result.version:
            logging.info(pkg_resources.get_distribution("sonic").version)
        elif parser_result.config:
            config.log()
        elif "setup" in parser_result.sequence:  # setup doesn't require a control file
            setup(parser_result.dryrun)
        else:
            with open(parser_result.file, "r") as ymlfile:
                sonic_model = yaml.load(ymlfile)
                if "tasks" not in sonic_model:
                    util.message(
                        "This doesn't look like a Sonic project, since no tasks have been defined in the control file (%s)" % parser_result.file)
                    sys.exit(2)
                if not parser_result.skip_login or parser_result.login:
                    login_if_needed(forced=parser_result.login, debug=parser_result.debug)
                context_args = args_to_dict(parser_result.context)
                init_context(sonic_model, context_args)
                for sequence in parser_result.sequence:
                    if sequence == "clean":
                        metrics.start("clean")
                        clean()
                        metrics.stop("clean")
                    else:
                        compose.with_pull = parser_result.pull
                        compose.task_config = get_task_config(sonic_model)
                        run_sequence(sequence, sonic_model, context_args)
    except IOError:
        util.message("The expected control file (%s) was not found in current directory" % parser_result.file)
        sys.exit(3)
    except SonicException as e:
        logging.error(e)
        sys.exit(e.exit_code())
    except Exception as e:
        logging.error(e, exc_info=True)
        sys.exit(5)
    finally:
        metrics.log()


def clean():
    compose.cleanup()


def run_sequence(sequence_name, sonic_model, context_args):
    sequences = config.get("sequences", {})
    sequences.update(sonic_model.get("sequences", {}))
    if sequence_name in sequences:
        for sequence in sequences.get(sequence_name):
            for pipe_name, definition in sequence.items():
                init_context(sonic_model, context_args)
                context = Context()
                context.update(definition.get("context", {}))
                context.pipe_id = util.generate_id()
                context.save()
                model = copy.deepcopy(sonic_model)
                model["tasks"].update(definition.get("tasks", {}))
                run_pipe(pipe_name, model)
                metrics.log()
                metrics.clear()
    else:
        run_pipe(sequence_name, sonic_model)


def run_pipe(pipe_name, sonic_model):
    pipes = config.get("pipes", {})
    pipes.update(sonic_model.get("pipes", {}))
    pipe_model = None
    if pipe_name in pipes:
        pipe_model = pipes[pipe_name]
        pipe_model.setdefault("tasks", {})
        if pipe_name in sonic_model.get("pipes", {}):
            pipe_model["tasks"] = sonic_model["pipes"][pipe_name].get("tasks", pipe_model["tasks"])
    elif pipe_name == "default":
        pipe_model = {"tasks": ["build", "test"]}
    elif pipe_name in sonic_model["tasks"]:
        pipe_model = {"tasks": [pipe_name]}

    if not pipe_model:
        raise PipeNotFoundException(pipe_name)

    context = Context()
    context.setdefault("pipe_id", util.generate_id())
    context.pipe = pipe_name
    context.save()

    if "pre" in pipe_model:
        run_encompassing_task("pre-" + pipe_name, pipe_model["pre"])
    try:
        for task_name in pipe_model["tasks"]:
            run_task(task_name, sonic_model)
    finally:
        if "post" in pipe_model:
            run_encompassing_task("post-" + pipe_name, pipe_model["post"])


def run_task(task_name, sonic_model):
    logging.debug("sonic_model:\n%s" % yaml.dump(sonic_model, default_flow_style=False, indent=4))

    if task_name not in sonic_model["tasks"]:
        logging.info("No %s task defined, moving on!" % task_name)
        return

    metrics.start(task_name)

    context = Context()
    context.task_id = util.generate_id()
    context.task = task_name
    context.status = 0
    context.save()

    run_pre_tasks(task_name, sonic_model)

    try:
        tasks = sonic_model["tasks"][task_name]
        do_task(task_name, tasks)
        context.refresh()
        context.status = 0
    except Exception:
        context.refresh()
        context.status = 1
        raise
    finally:
        context.save()
        run_post_tasks(task_name, sonic_model)
        del context.task
        del context.task_id
        context.save()
        metrics.stop(task_name, context.status)


def get_task_config(sonic_model):
    task_config = sonic_model["task-config"] if "task-config" in sonic_model else {
        'shm_size': config.get("shm_size") or "512m",
        'mem_limit': config.get("mem_limit") or "2048m"
    }
    return task_config


def do_task(task_name, tasks):
    if isinstance(tasks, str):
        model = compose.create_model(task_name, tasks)
        compose.run(task_name, model)
    elif isinstance(tasks, list):
        for task_index, task in enumerate(tasks):
            model = compose.create_model(task_name, task, task_index)
            compose.run(task_name, model, task_index)
    elif isinstance(tasks, dict):
        model = compose.create_model(task_name, tasks)
        compose.run(task_name, model)


def run_pre_tasks(task_name, sonic_model):
    pre_task = find_encompassing_task("pre", task_name, sonic_model)
    if pre_task:
        run_encompassing_task("pre" + "-" + task_name, pre_task)


def run_post_tasks(task_name, sonic_model):
    pre_task = find_encompassing_task("post", task_name, sonic_model)
    if pre_task:
        run_encompassing_task("post" + "-" + task_name, pre_task)


def find_encompassing_task(prefix, task_name, sonic_model):
    task = []

    def add(step):
        if isinstance(step, list):
            task.extend(step)
        else:
            task.append(step)

    if prefix + "-" + task_name in sonic_model["tasks"]:
        add(sonic_model["tasks"][prefix + "-" + task_name])

    config_tasks = config.get("tasks")
    if config_tasks:
        if prefix + "-" + task_name in config_tasks:
            add(config_tasks[prefix + "-" + task_name])
        elif prefix + "-task" in config_tasks:
            add(config_tasks[prefix + "-task"])

    return task


def run_encompassing_task(task_name, task_definition):
    try:
        compose.log_level = logging.DEBUG
        if isinstance(task_definition, list):
            for task_index, task in enumerate(task_definition):
                try:
                    do_task(task_name + "-" + str(task_index), task)
                except NonZeroExitCodeException as error:
                    logging.warn("%s-%s exited with exit code (%s)" % (task_name, task_index, error.exit_code()))
        elif task_definition:
            try:
                do_task(task_name, task_definition)
            except NonZeroExitCodeException as error:
                logging.warn("%s exited with exit code (%s)" % (task_name, error.exit_code()))
    finally:
        compose.log_level = logging.INFO


def setup(dryrun):
    if util.get_user_id() > 0:
        util.message("The setup must be run as 'sudo $(which sonic) setup'")
        exit(1)
    if dryrun:
        util.message("Doing a setup dry-run")
    try:
        user = os.environ['SUDO_USER']
        uid = int(os.environ['SUDO_UID'])
        # gid = int(os.environ['SUDO_GID'])
        #
        # Add "userns-remap": "${USER}" to /etc/docker/daemon.json
        #
        daemon_json_file_location = util.get_docker_daemon_json_location()
        deamon_config = util.load_json(daemon_json_file_location) or dict()
        deamon_config["userns-remap"] = user
        deamon_config["mtu"] = 1400
        util.message("Storing the following in %s:" % daemon_json_file_location)
        json.dump(deamon_config, sys.stdout, indent=2)
        util.newline()  # Add extra newline
        if not dryrun:
            util.store_as_json(deamon_config, daemon_json_file_location)
        #
        # Put ${USER}:$(id -u):65536 into /etc/subuid
        #
        pattern = "%s:\d+:\d+" % user
        required_line = "%s:%s:%s" % (user, uid, 65536)
        util.replace_add(pattern, required_line, "/etc/subuid", dryrun)
        #
        # Put ${USER}:$(( ${docker.groupId} )):65536 into /etc/subgid
        #
        required_line = "%s:%s:%s" % (user, util.get_docker_group_id(), 65536)
        util.replace_add(pattern, required_line, "/etc/subgid", dryrun)
        #
        # Restart the docker daemon
        #
        util.message("Restarting the docker daemon")
        docker_restart_command = "service docker restart"
        if dryrun:
            util.command(docker_restart_command)
        else:
            ec_docker_restart, output = util.run(docker_restart_command)
            if ec_docker_restart > 0:
                raise Exception("Error restarting Docker: %s" % output)
        util.message("Completed setup.")
    except Exception as error:
        logging.exception(error)
