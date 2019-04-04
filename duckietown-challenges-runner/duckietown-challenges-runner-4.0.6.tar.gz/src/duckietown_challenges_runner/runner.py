#!/usr/bin/env python
# coding=utf-8

import argparse
import copy
import getpass
import json
import logging
import mimetypes
import os
import platform
import random
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import traceback
from collections import OrderedDict
from contextlib import contextmanager
from typing import List, Optional

import docker
import termcolor
import yaml
from six import BytesIO

from dt_shell import UserError
from dt_shell.constants import DTShellConstants
from dt_shell.env_checks import check_executable_exists, InvalidEnvironment, check_docker_environment
from duckietown_challenges import ChallengesConstants
from duckietown_challenges.challenge import EvaluationParameters, SUBMISSION_CONTAINER_TAG
from duckietown_challenges.challenge_results import read_challenge_results, ChallengeResults, \
    NoResultsFound
from duckietown_challenges.cmd_submit_build import parse_complete_tag, get_complete_tag
from duckietown_challenges.constants import CHALLENGE_SOLUTION_OUTPUT_DIR, CHALLENGE_RESULTS_DIR, \
    CHALLENGE_DESCRIPTION_DIR, \
    CHALLENGE_EVALUATION_OUTPUT_DIR, ENV_CHALLENGE_NAME, ENV_CHALLENGE_STEP_NAME, CHALLENGE_PREVIOUS_STEPS_DIR, \
    DEFAULT_DTSERVER
from duckietown_challenges.rest_methods import dtserver_work_submission, dtserver_report_job
from duckietown_challenges.utils import friendly_size, indent
from . import __version__
from .runner_cache import copy_to_cache, get_file_from_cache

logging.basicConfig()
elogger = logging.getLogger('evaluator')
elogger.setLevel(logging.DEBUG)


def get_token_from_shell_config():
    k = DTShellConstants.DT1_TOKEN_CONFIG_KEY

    if k in os.environ:
        # msg = 'Using token passed in environment variable %s' % k
        # elogger.debug(msg)
        return os.environ[k]
    else:
        pass
        # msg = 'Could not find the env variable %s; reading shell config.' % k
        # elogger.debug(msg)

    path = os.path.join(os.path.expanduser(DTShellConstants.ROOT), 'config')
    if not os.path.exists(path):
        msg = 'Could not find the shell config at %s' % path
        raise Exception(msg)

    data = open(path).read()
    config = json.loads(data)

    if k not in config:
        msg = 'Please set a Duckietown Token using the command `dts tok set`.'
        raise Exception(msg)
    else:
        return config[k]


def dt_challenges_evaluator():
    try:
        dt_challenges_evaluator_()
    except SystemExit:  # --help
        raise
    except BaseException:
        msg = traceback.format_exc()
        elogger.error(msg)
        sys.exit(2)


def dt_challenges_evaluator_():
    from duckietown_challenges.col_logging import setup_logging
    setup_logging()
    elogger.info("dt-challenges-evaluator (DTC %s)" % __version__)
    elogger.info('called with:\n%s' % sys.argv)

    usage = """
    
Usage:
    
"""
    args = sys.argv[1:]
    if args and args[0].startswith('dt-'):
        elogger.debug('removing first arg from %s' % args)
        args = args[1:]
    prog = 'dt-challenges-evaluator'
    parser = argparse.ArgumentParser(prog=prog, usage=usage)
    parser.add_argument("--version", action="store_true", default=False)
    parser.add_argument("--continuous", action="store_true", default=False)
    parser.add_argument("--no-pull", dest='no_pull', action="store_true", default=False)
    parser.add_argument("--no-upload", dest='no_upload', action="store_true", default=False)
    parser.add_argument("--no-delete", dest='no_delete', action="store_true", default=False)
    parser.add_argument("--machine-id", default=None, help='Machine name')
    parser.add_argument("--name", default=None, help='Evaluator name')
    parser.add_argument("--submission", default=None, help='evaluate this particular submission')
    parser.add_argument("--reset", dest='reset', action="store_true", default=False,
                        help='Reset submission')
    parser.add_argument("--features", default='{}')
    parser.add_argument("--debug-volumes", default=None)
    parsed = parser.parse_args(args=args)
    if parsed.submission and parsed.continuous:
        msg = 'Cannot specify both --submission and --continuous.'
        raise UserError(msg)
    if parsed.version:
        msg = 'Duckietown Challenges Runner %s' % __version__
        from duckietown_challenges import __version__ as dcversion
        msg += '\nDuckietown Challenges %s' % dcversion
        print(msg)
        return

    check_docker_environment()
    try:
        check_executable_exists('docker-compose')
    except InvalidEnvironment:
        msg = 'Could not find docker-compose. Please install it.'
        msg += '\n\nSee: https://docs.docker.com/compose/install/#install-compose'
        raise InvalidEnvironment(msg)

    tmpdir = '/tmp/duckietown/DT18/evaluator/executions'

    try:
        more_features = yaml.load(parsed.features, Loader=yaml.SafeLoader)
    except BaseException as e:
        msg = 'Could not evaluate your YAML string %r:\n%s' % (parsed.features, e)
        raise Exception(msg)

    if not isinstance(more_features, dict):
        msg = 'I expected that the features are a dict; obtained %s: %r' % (type(more_features).__name__, more_features)
        raise Exception(msg)

    do_pull = not parsed.no_pull
    do_upload = not parsed.no_upload
    delete = not parsed.no_delete
    reset = parsed.reset
    evaluator_name = parsed.name or 'p-%s' % os.getpid()
    machine_id = parsed.machine_id or socket.gethostname()

    token = get_token_from_shell_config()

    args = dict(do_upload=do_upload, do_pull=do_pull, more_features=more_features,
                delete=delete, evaluator_name=evaluator_name, machine_id=machine_id,
                tmpdir=tmpdir, token=token, debug_volumes=parsed.debug_volumes)
    ndots = 0

    if parsed.continuous:

        timeout = 5.0  # seconds
        multiplier = 1.0
        multiplier_grow = 1.5
        max_multiplier = 5
        while True:
            multiplier = min(multiplier, max_multiplier)
            t0 = time.time()
            try:
                go_(None, reset=False, **args)
                multiplier = 1.0
            except NothingLeft:
                delta = time.time() - t0

                sys.stderr.write('No work for me yet. Server answers in %.1f seconds.\n' % delta)
                ndots += 1
                if ndots == 5:
                    # sys.stderr.write(' no work for me yet.\n')
                    ndots = 0
                # time.sleep(timeout * multiplier)
                # elogger.info('No submissions available to evaluate.')
            except ConnectionError as e:
                elogger.error(e)
                multiplier *= multiplier_grow
            except BaseException:
                msg = 'Uncaught exception:\n%s' % traceback.format_exc()
                elogger.error(msg)
                multiplier *= multiplier_grow

            r = random.random() * 2
            time.sleep(timeout * multiplier + r)

    else:
        if parsed.submission:
            submissions = [parsed.submission]
        else:
            submissions = [None]

        for submission_id in submissions:
            try:
                go_(submission_id, reset=reset, **args)
            except NothingLeft as e:
                if submission_id is None:
                    msg = 'No submissions available to evaluate.'
                else:
                    msg = 'Could not evaluate submission %s.' % submission_id

                msg += '\n' + str(e)
                elogger.error(msg)


class NothingLeft(Exception):
    pass


def get_features(more_features):
    import psutil

    features = {}

    machine = platform.machine()
    features['linux'] = sys.platform.startswith('linux')
    features['mac'] = sys.platform.startswith('darwin')
    features['x86_64'] = (machine == 'x86_64')
    features['armv7l'] = (machine == 'armv7l')
    meminfo = psutil.virtual_memory()
    # svmem(total=16717422592, available=5376126976, percent=67.8, used=10359984128, free=1831890944, active=7191916544, inactive=2325667840, buffers=525037568, cached=4000509952, shared=626225152)

    features['ram_total_mb'] = int(meminfo.total / (1024 * 1024.0))
    features['ram_available_mb'] = int(meminfo.available / (1024 * 1024.0))
    features['nprocessors'] = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    if cpu_freq is not None:
        # None on Docker
        features['processor_frequency_mhz'] = int(psutil.cpu_freq().max)
    f = psutil.cpu_percent(interval=0.2)
    features['processor_free_percent'] = int(100.0 - f)
    features['p1'] = True

    disk = psutil.disk_usage(os.getcwd())

    features['disk_total_mb'] = disk.total / (1024 * 1024)
    features['disk_available_mb'] = disk.free / (1024 * 1024)
    features['picamera'] = False
    features['nduckiebots'] = False
    features['map_3x3'] = False

    features['gpu'] = os.path.exists('/proc/driver/nvidia/version')

    for k, v in more_features.items():
        if k in features:
            msg = 'Using %r = %r instead of %r' % (k, more_features[k], features[k])
            # elogger.info(msg)
        features[k] = v

    # elogger.debug(json.dumps(features, indent=4))

    return features


class DockerComposeFail(Exception):
    pass


def get_FORMAT_datefmt():
    pre = '%(asctime)s|%(name)s|%(filename)s:%(lineno)s|%(funcName)s(): '
    pre = termcolor.colored(pre, attrs=['dark'])
    FORMAT = pre + "%(message)s"
    datefmt = "%H:%M:%S"
    return FORMAT, datefmt


@contextmanager
def setup_logging(wd):
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    if not os.path.exists(wd):
        os.makedirs(wd)
    f_stderr = os.path.join(wd, 'stderr.log')
    f_stdout = os.path.join(wd, 'stdout.log')

    my_stderr = Tee(os.path.join(wd, 'stderr.log'), sys.stderr)
    sys.stderr = my_stderr
    my_stdout = Tee(os.path.join(wd, 'stdout.log'), sys.stdout)
    sys.stdout = my_stdout
    ch = logging.StreamHandler(sys.stderr.file)

    ch.setLevel(logging.DEBUG)

    root = logging.getLogger()
    FORMAT, datefmt = get_FORMAT_datefmt()
    formatter = logging.Formatter(FORMAT, datefmt=datefmt)
    ch.setFormatter(formatter)
    root.addHandler(ch)

    try:
        yield
    finally:
        #
        my_stdout.flush()
        my_stderr.flush()

        # for s in [my_stderr, my_stdout]:
        #     try:
        #         fn = os.path.splitext(s.name)[0] + '.html'
        #         with open(fn, 'w') as f:
        #             from ansi2html import Ansi2HTMLConverter
        #             conv = Ansi2HTMLConverter()
        #             v = s.getvalue().strip()
        #             if not v:
        #                 v = '(No output was produced.)'
        #             html = conv.convert(v)
        #             f.write(html)
        #         os.remove(s.name)
        #     except:
        #         pass

        sys.stderr = old_stderr
        sys.stdout = old_stdout
        root.removeHandler(ch)

    def convert(log):
        fn = os.path.splitext(log)[0] + '.html'
        data = open(log).read().strip()

        from ansi2html import Ansi2HTMLConverter
        conv = Ansi2HTMLConverter()
        if not data:
            data = '(No output was produced.)'
        html = conv.convert(data)
        with open(fn, 'w') as f:
            f.write(html)
        # os.remove(log)

    convert(f_stdout)
    convert(f_stderr)


def go_(submission_id, do_pull, more_features, do_upload, delete, reset, evaluator_name, machine_id, tmpdir,
        token=None, debug_volumes: Optional[str] = None):
    features = get_features(more_features)
    if features['processor_free_percent'] < 50:
        elogger.info(f"Waiting because free CPU is {features['processor_free_percent']}%.")
        return

    if token is None:
        token = get_token_from_shell_config()
    from duckietown_challenges import __version__ as version_dc
    from . import __version__ as version_dcr
    from dt_shell import __version__ as version_dts

    evaluator_version = 'DC:%s;DCR:%s;DTS:%s' % (version_dcr, version_dc, version_dts)
    process_id = evaluator_name

    timeout_server = 60
    res = dtserver_work_submission(token, submission_id, machine_id, process_id, evaluator_version,
                                   features=features, reset=reset, timeout=timeout_server)

    if 'job_id' not in res:
        msg = 'Could not find jobs: %s' % res['msg']
        raise NothingLeft(msg)

    job_id = res['job_id']
    elogger.info(json.dumps(res, indent=2))

    challenge_name = res['challenge_name']
    challenge_step_name = res['step_name']
    submission_id = res['submission_id']

    elogger.info('Evaluating job %s' % job_id)

    uploaded = []
    try:

        steps2artefacts = res['steps2artefacts']

        locations = res['parameters']['locations']
        location = locations[0]
        organization = location['organization']
        repository = location['repository']
        tag = location['tag']
        digest = location['digest']
        registry = location['registry']

        if registry == 'dockerhub':
            solution_container = '%s/%s:%s' % (organization, repository, tag)
        # solution_container = '%s/%s:%s@%s' % (organization, repository, tag, digest)
        else:
            solution_container = '%s/%s/%s:%s' % (registry, organization, repository, tag)
        elogger.info('solution_container = %s' % solution_container)

        wd = os.path.join(tmpdir, challenge_name, 'submission%d' % submission_id,
                          '%s-%s-job%s' % (challenge_step_name, evaluator_name, job_id))

        if not os.path.exists(wd):
            os.makedirs(wd)

        own_logs_dir = os.path.join(wd, 'logs', 'challenges-runner')

        aws_config = res['aws_config']
        if aws_config and do_upload:
            try_s3(aws_config)

        try:

            with setup_logging(own_logs_dir):
                challenge_parameters_ = EvaluationParameters.from_yaml(res['challenge_parameters'])

                project = 'job%s-%s' % (job_id, random.randint(1, 10000))
                if not do_upload:
                    aws_config = None

                cr = run_single(wd, aws_config, steps2artefacts, challenge_parameters_, solution_container,
                                challenge_name,
                                challenge_step_name, project, do_pull, debug_volumes=debug_volumes)
        finally:
            if do_upload:
                uploaded = upload_files(wd, aws_config)

        if delete:
            cmd = ['down']
            run_docker(wd, project, cmd)

        if delete:
            shutil.rmtree(wd)
        else:
            msg = f'I will not delete temporary dir {wd}'
            elogger.info(msg)

    except KeyboardInterrupt:
        msg = 'KeyboardInterrupt:\n%s' % traceback.format_exc()
        elogger.error(msg)
        status = ChallengesConstants.STATUS_JOB_ABORTED
        cr = ChallengeResults(status, msg, scores={})

    except BaseException:
        msg = 'Uncaught exception:\n%s' % traceback.format_exc()
        elogger.error(msg)
        status = ChallengesConstants.STATUS_JOB_HOST_ERROR
        cr = ChallengeResults(status, msg, scores={})

    msg = ('Reporting status %s for job %s step %s submission %s.\n\n%s\n\n%s' %
           (cr.get_status(), job_id, challenge_step_name, submission_id,
            indent(cr.msg, ' msg |'), indent(json.dumps(cr.get_stats(), indent=4), 'stats |')))
    if cr.get_status() != ChallengesConstants.STATUS_JOB_SUCCESS:
        elogger.error(msg)
    else:
        elogger.info(msg)

    stats = cr.get_stats()
    # REST call to the duckietown chalenges server
    ntries = 5
    interval = 10
    while ntries >= 0:
        try:
            dtserver_report_job(token,
                                job_id=job_id,
                                stats=stats,
                                result=cr.get_status(),
                                machine_id=machine_id,
                                process_id=process_id,
                                evaluator_version=evaluator_version,
                                uploaded=uploaded,
                                timeout=timeout_server)
            break
        except BaseException as e:
            msg = 'Could not report: %s' % e
            elogger.warning(msg)
            elogger.info('Retrying %s more times after %s seconds' % (ntries, interval))
            ntries -= 1
            time.sleep(interval)


def run_single(wd, aws_config, steps2artefacts, challenge_parameters, solution_container, challenge_name,
               challenge_step_name, project, do_pull, debug_volumes: Optional[str] = None):
    prepare_dir(wd, aws_config, steps2artefacts)
    tomonitor = []
    for service_name, service_def in challenge_parameters.services.items():
        if service_def.image == SUBMISSION_CONTAINER_TAG:
            continue
        else:
            tomonitor.append(service_name)
    config = get_config(challenge_parameters, solution_container, challenge_name, challenge_step_name,
                        debug_volumes=debug_volumes)
    config_yaml = yaml.safe_dump(config, encoding='utf-8', indent=4, allow_unicode=True)
    if isinstance(config_yaml, bytes):
        config_yaml = config_yaml.decode('utf-8')
    # elogger.debug('YAML:\n' + config_yaml)

    dcfn_original = os.path.join(wd, 'docker-compose.original.yaml')
    dcfn = os.path.join(wd, 'docker-compose.yaml')

    # elogger.info('Compose file: \n%s ' % compose)
    with open(dcfn_original, 'w') as f:
        f.write(config_yaml)
    with open(dcfn, 'w') as f:
        f.write(config_yaml)

    # validate the configuration

    try:
        config_validated = run_docker(wd, project, ['config'], get_output=True).decode('utf-8')
        with open(dcfn, 'w') as f:
            f.write(config_validated)
        elogger.info('config:\n%s' % config_validated)
        valid_config = True
        valid_config_error = None
    except DockerComposeFail:
        valid_config_error = 'Could not validate Docker Compose configuration:\n%s' % traceback.format_exc()
        elogger.error(valid_config_error)
        valid_config = False

    if valid_config:
        services_names = list(challenge_parameters.services)
        # print('services: %s' % services_names)
        cr = run_one(wd, project, do_pull, services=services_names, monitor=tomonitor[0])

        write_logs(wd, project, services=config['services'])
    else:
        status = ChallengesConstants.STATUS_JOB_ERROR

        cr = ChallengeResults(status, valid_config_error, scores={})
    return cr


def get_id_for_service(wd, project, service_name) -> str:
    cmd = ['ps', '-q', service_name]

    try:
        o = run_docker(wd, project, cmd, get_output=True)
        container_id = o.decode('utf-8').strip()  # \n at the end
    except DockerComposeFail:
        raise
    return container_id


class EvaluatorTimeout(Exception):
    pass


def write_logs_worker(service_name, container_id):
    elogger.info('writing logs for %s ' % container_id)

    client = check_docker_environment()
    from dateutil import parser
    container = client.containers.get(container_id)
    for x in container.logs(stream=True, stdout=True, stderr=True,
                            timestamps=True):
        x = x.decode('utf-8')
        i = x.index(' ')
        timestamp = x[:i]
        message = x[i + 1:].rstrip()  # \n
        ts = parser.parse(timestamp)
        s = "%s %s %s" % (ts.strftime('%H:%M:%S'), service_name, message)
        print(s)
        if container.status != 'running':
            break

    exit_code = exit_code_for_container(container_id)

    elogger.info('container %s terminated with %s' % (service_name, exit_code))


def exit_code_for_container(container_id):
    cmd = ['docker', 'inspect', container_id, "--format={{.State.ExitCode}}"]
    out = subprocess.check_output(cmd)
    return int(out.strip())


class Workers(object):
    workers = []


def stream_logs(service_name, container_id):
    from multiprocessing import Process
    p = Process(target=write_logs_worker, args=(service_name, container_id,))
    p.start()
    Workers.workers.append(p)


def teminate_workers():
    for p in list(Workers.workers):
        elogger.debug('terminating %s' % p)
        Workers.workers.remove(p)
        p.terminate()
    elogger.debug('terminated all workers.')


DEFAULT_TIMEOUT = 1800


def run_one(wd, project, do_pull, monitor, services, timeout=DEFAULT_TIMEOUT):
    client = check_docker_environment()

    # noinspection PyBroadException
    try:
        if do_pull:
            elogger.info('pulling containers')
            cmd = ['pull',  # '--ignore-pull-failures'
                   ]
            run_docker(wd, project, cmd)

        try:
            pruned = client.networks.prune(filters=dict(until='1h'))
            elogger.debug('pruned: %s' % pruned)
        except BaseException as e:  # XXX not critical
            pass

        # elogger.info('Creating containers')
        # cmd = ['create', '--force-recreate']
        # run_docker(wd, project, cmd)

        elogger.info('Running containers %s' % services)
        cmd = ['up',
               '-d',
               # '--remove-orphans',
               # '--abort-on-container-exit'
               ]
        run_docker(wd, project, cmd)

        service2id = {}
        for service_name in services:
            service2id[service_name] = get_id_for_service(wd, project, service_name)
            stream_logs(service_name, service2id[service_name])
        t0 = time.time()

        client = check_docker_environment()
        while True:
            exited = []
            running = []
            should_break = False
            for service_name, container_id in service2id.items():
                container = client.containers.get(container_id)
                # msg = 'service %s: %s' % (service_name, container.status)
                # elogger.debug(msg)
                if container.status != 'running':
                    exited.append(service_name)
                    exit_code = exit_code_for_container(container_id)
                    if exit_code:
                        msg = '%s exited with code %s' % (service_name, exit_code)
                        elogger.error(msg)
                        should_break = True
                else:
                    running.append(service_name)

            msg = 'Services running: %s  exited:  %s' % (running, exited)
            elogger.debug(msg)
            if should_break:
                break

            if monitor in exited:
                break

            delta = time.time() - t0
            if delta > timeout:
                msg = 'Waited %s for container to finish. Giving up. ' % delta
                raise EvaluatorTimeout(msg)

            time.sleep(4)

        try:
            cr = read_challenge_results(wd)
        except NoResultsFound:
            msg = '''\
The result file is not found. This usually means that the evaluator did not finish
and some times that there was an import error.

Check the evaluator log to see what happened.'''
            elogger.error(msg)
            status = ChallengesConstants.STATUS_JOB_ERROR
            cr = ChallengeResults(status, msg, scores={})

    except EvaluatorTimeout as e:
        msg = 'Timeout:\n\n%s' % e
        elogger.error(msg)
        status = ChallengesConstants.STATUS_JOB_ERROR
        cr = ChallengeResults(status, msg, scores={})
    except DockerComposeFail as e:
        msg = 'Error while running Docker Compose:\n\n%s' % e
        elogger.error(msg)
        status = ChallengesConstants.STATUS_JOB_HOST_ERROR
        cr = ChallengeResults(status, msg, scores={})

    except KeyboardInterrupt:
        msg = 'KeyboardInterrupt:\n%s' % traceback.format_exc()
        elogger.error(msg)
        status = ChallengesConstants.STATUS_JOB_ABORTED
        cr = ChallengeResults(status, msg, scores={})

    except BaseException:  # XXX
        msg = 'Uncaught exception while running Docker Compose:\n%s' % traceback.format_exc()
        elogger.error(msg)
        status = ChallengesConstants.STATUS_JOB_HOST_ERROR
        cr = ChallengeResults(status, msg, scores={})
    finally:
        teminate_workers()

    return cr


def prepare_dir(wd, aws_config, steps2artefacts):
    if not os.path.exists(wd):
        os.makedirs(wd)
    # output for the sub
    challenge_solution_output_dir = os.path.join(wd, CHALLENGE_SOLUTION_OUTPUT_DIR)
    # the yaml with the scores
    challenge_results_dir = os.path.join(wd, CHALLENGE_RESULTS_DIR)
    # the results of the "preparation" step
    challenge_description_dir = os.path.join(wd, CHALLENGE_DESCRIPTION_DIR)
    challenge_evaluation_output_dir = os.path.join(wd, CHALLENGE_EVALUATION_OUTPUT_DIR)
    previous_steps_dir = os.path.join(wd, CHALLENGE_PREVIOUS_STEPS_DIR)

    for d in [challenge_solution_output_dir, challenge_results_dir, challenge_description_dir,
              challenge_evaluation_output_dir, previous_steps_dir]:
        if not os.path.exists(d):
            os.makedirs(d)

    download_artefacts(aws_config, steps2artefacts, previous_steps_dir)


def get_config(challenge_parameters_, solution_container, challenge_name, challenge_step_name,
               debug_volumes: Optional[str] = None):
    # client = docker.from_env()
    # from docker.errors import NotFound
    # Adding the submission container
    for service_def in challenge_parameters_.services.values():
        service_def.build = None

        if service_def.image == SUBMISSION_CONTAINER_TAG:
            service_def.image = solution_container

    config = challenge_parameters_.as_dict()

    # do_trick = False
    for service in config['services'].values():
        image = service['image']
        br = parse_complete_tag(image)
        br.digest = None
        service['image'] = get_complete_tag(br)
        #
        # if do_trick:
        #     if image_digest:
        #         # If we have the image then we don't bother with pulling the tag
        #         try:
        #             c = client.images.get(image_digest)
        #         except NotFound:
        #             msg = 'Could not find the image for %s by digest %s; will need to pull.' % (
        #                 service['image'], image_digest)
        #             elogger.info(msg)
        #         else:
        #             msg = 'I already have the exact image for %s' % service['image']
        #             elogger.info(msg)
        #             #
        #             #
        #             if True:
        #
        #                 n = len('91bac885982d')
        #                 partial_id = image_digest.replace('sha256:', '')[:n]
        #                 service['image'] = partial_id
        #             else:
        #                 image = service['image']
        #                 # remove tag
        #                 if ':' in image:
        #                     image = image.split(':')[0]
        #                 service['image'] = image + '@' + image_digest

        service.pop('build', None)

        # if service['image'] == SUBMISSION_CONTAINER_TAG:
        #     service['image'] = solution_container

        # This is not needed, because the tag is sufficient as it is generated anew.
        # We should perhaps check that we have the right image tag
        #
        # if image_digest is not None:
        #     service['image'] += '@' + image_digest
    # else:
    #     msg = 'Cannot find the tag %s' % SUBMISSION_CONTAINER_TAG
    #     elogger.warning(msg)
    #     # raise Exception(msg)

    # adding extra environment variables:
    UID = os.getuid()
    USERNAME = getpass.getuser()
    extra_environment = dict(username=USERNAME, uid=UID)
    extra_environment[ENV_CHALLENGE_NAME] = challenge_name
    extra_environment[ENV_CHALLENGE_STEP_NAME] = challenge_step_name

    for service in config['services'].values():
        service['environment'].update(extra_environment)

    # add volumes

    volumes = [
        '.:/challenges',
        'fifos:/fifos'
    ]

    if debug_volumes:
        data = yaml.load(open(debug_volumes).read(), Loader=yaml.SafeLoader)
        volumes.extend(data['volumes'])

    for service in config['services'].values():
        assert 'volumes' not in service
        service['volumes'] = copy.deepcopy(volumes)

    # elogger.info('Now:\n%s' % safe_yaml_dump(config))

    NETWORK_NAME = 'evaluation'
    networks_evaluator = dict(evaluation=dict(aliases=[NETWORK_NAME]))
    for service in config['services'].values():
        service['networks'] = copy.deepcopy(networks_evaluator)
    config['networks'] = dict(evaluation=None)
    config['volumes'] = dict(fifos=None)
    return config


def write_logs(wd, project, services):
    client = check_docker_environment()

    logdir = os.path.join(wd, 'logs')
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    for service in services:
        container_id = get_id_for_service(wd, project, service)

        # cmd = ['ps', '-q', service]
        # try:
        #     o = run_docker(wd, project, cmd, get_output=True)
        #     container_id = o.strip()  # \n at the end
        # except DockerComposeFail:
        #     continue

        if not container_id:
            logs = 'Service "%s" was not started.' % service
            elogger.warning(logs)
        else:
            # elogger.info('Found container ID = %r' % container_id)

            for fname, options in [
                ('combined', dict(stderr=True, stdout=True)),
                ('stderr', dict(stderr=True, stdout=False)),
                ('stdout', dict(stdout=True, stderr=False)),
            ]:

                logs = logs_for_container(client, container_id, **options)

                from ansi2html import Ansi2HTMLConverter
                conv = Ansi2HTMLConverter()
                html = conv.convert(logs)

                logdir_service = os.path.join(logdir, service)
                if not os.path.exists(logdir_service):
                    os.makedirs(logdir_service)
                fn = os.path.join(logdir_service, '%s.log' % fname)
                with open(fn, 'w') as f:
                    f.write(logs)

                fn = os.path.join(logdir_service, '%s.html' % fname)
                with open(fn, 'w') as f:
                    f.write(html)


class Tee:
    def __init__(self, name, f):
        self.file = open(name, 'w')
        self.name = name
        self.original = f

    def close(self):
        if hasattr(self, 'file'):
            if self.file is not None:
                self.file.close()
                self.file = None

    def __del__(self):
        self.close()

    def write(self, data: str):
        # if isinstance(data, str):
        #     data = data.encode('utf-8')
        self.file.write(data)
        self.file.flush()
        # data_s = data.decode('utf-8')
        self.original.write(data)
        self.original.flush()

    def flush(self):
        self.file.flush()
        self.original.flush()

    def fileno(self):
        return self.file.fileno()

    def getvalue(self):
        with open(self.name) as f:
            return f.read()


def run_docker(cwd: str, project: str, cmd0: List[str], get_output=False) -> bytes:
    cmd0 = ['docker-compose', '-p', project] + cmd0
    # elogger.info('Running:\n\t%s' % " ".join(cmd0) + '\n\n in %s' % cwd)
    # elogger.debug('Running: %s' % " ".join(cmd0))

    d = tempfile.mkdtemp()

    fn1 = os.path.join(d, 'docker-stdout.txt')
    fn2 = os.path.join(d, 'docker-stderr.txt')
    # elogger.debug('Saving stdout to %s' % fn1)

    # with StdoutTee(fn1), StderrTee(fn2):

    tee_stdout = Tee(fn1, sys.stdout)
    tee_stderr = Tee(fn2, sys.stderr)

    try:
        if get_output:
            return subprocess.check_output(cmd0, cwd=cwd, stderr=sys.stderr)
        else:
            # noinspection PyTypeChecker
            subprocess.check_call(cmd0, cwd=cwd, stdout=tee_stdout, stderr=tee_stderr)
    except subprocess.CalledProcessError as e:
        msg = 'Could not run %s:\n\n %s' % (cmd0, indent(e, '  >  '))
        msg += '\n\n%s' % indent(tee_stdout.getvalue(), 'stdout | ')
        msg += '\n\n%s' % indent(tee_stderr.getvalue(), 'stderr | ')
        raise DockerComposeFail(msg)
    finally:
        try:
            os.unlink(fn1)
            os.unlink(fn2)
        except:
            pass
        pass


def upload_files(wd, aws_config, ignore_patterns=('.DS_Store',)):
    toupload = get_files_to_upload(wd, ignore_patterns=ignore_patterns)

    if not aws_config:
        msg = 'Not uploading artifacts because AWS config not passed.'
        elogger.info(msg)
        uploaded = only_copy_to_cache(toupload)
    else:
        uploaded = upload(aws_config, toupload)

    return uploaded


class CouldNotDownloadAll(Exception):
    pass


def download_artefacts(aws_config, steps2artefacts, wd):
    for step_name, artefacts in steps2artefacts.items():
        step_dir = os.path.join(wd, step_name)
        os.makedirs(step_dir)
        for rpath, data in artefacts.items():
            # elogger.debug(data)
            fn = os.path.join(step_dir, rpath)
            dn = os.path.dirname(fn)
            if not os.path.exists(dn):
                os.makedirs(dn)

            sha256hex = data['sha256hex']
            size = data['size']
            storage = data['storage']

            try:
                get_file_from_cache(fn, sha256hex)
                elogger.info('cache   %7s   %s' % (friendly_size(size), rpath))
            except KeyError:

                # no local
                if 's3' in storage:
                    if not aws_config:
                        msg = 'I cannot download from S3 because credentials not given.'
                        raise CouldNotDownloadAll(msg)
                    else:
                        s3ob = storage['s3']
                        bucket_name = s3ob['bucket_name']
                        object_key = s3ob['object_key']

                        elogger.info('AWS     %7s   %s' % (friendly_size(size), rpath))
                        get_object(aws_config, bucket_name, object_key, fn)
                        copy_to_cache(fn, sha256hex)

                    size_now = os.stat(fn).st_size
                    if size_now != size:
                        msg = 'Corrupt cache or download for %s at %s.' % (data, fn)
                        raise ValueError(msg)
                else:
                    msg = 'Not in cache and no way to download'
                    raise CouldNotDownloadAll(msg)


def try_s3(aws_config):
    bucket_name = aws_config['bucket_name']
    aws_access_key_id = aws_config['aws_access_key_id']
    aws_secret_access_key = aws_config['aws_secret_access_key']
    aws_root_path = aws_config['path']
    import boto3
    s3 = boto3.resource("s3",
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)

    s = b'initial data'
    data = BytesIO(s)
    elogger.debug('trying bucket connection')
    s3_object = s3.Object(bucket_name, os.path.join(aws_root_path, 'initial.txt'))
    s3_object.upload_fileobj(data)
    elogger.debug('uploaded')


def get_object(aws_config, bucket_name, object_key, fn):
    aws_access_key_id = aws_config['aws_access_key_id']
    aws_secret_access_key = aws_config['aws_secret_access_key']
    import boto3
    s3 = boto3.resource("s3",
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)
    aws_object = s3.Object(bucket_name, object_key)
    aws_object.download_file(fn)


def get_files_to_upload(path, ignore_patterns=()):
    def to_ignore(x):
        for p in ignore_patterns:
            if os.path.basename(x) == p:
                return True
        return False

    toupload = OrderedDict()
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            if to_ignore(f):
                continue
            rpath = os.path.join(os.path.relpath(dirpath, path), f)
            if rpath.startswith('./'):
                rpath = rpath[2:]

            if CHALLENGE_PREVIOUS_STEPS_DIR in rpath:
                continue

            toupload[rpath] = os.path.join(dirpath, f)
    return toupload


def logs_for_container(client, container_id, stdout, stderr) -> str:
    container = client.containers.get(container_id)
    logs = container.logs(stdout=stdout, stderr=stderr, timestamps=True)
    return logs.decode('utf-8')


def only_copy_to_cache(toupload):
    uploaded = []
    for rpath, realfile in toupload.items():
        sha256hex = compute_sha256hex(realfile)
        copy_to_cache(realfile, sha256hex)
        size = os.stat(realfile).st_size
        mime_type = guess_mime_type(realfile)
        storage = {}
        uploaded.append(dict(size=size,
                             mime_type=mime_type, rpath=rpath, sha256hex=sha256hex, storage=storage))
    return uploaded


def guess_mime_type(filename):
    mime_type, _encoding = mimetypes.guess_type(filename)

    if mime_type is None:
        if filename.endswith('.yaml'):
            mime_type = 'text/yaml'
        else:
            mime_type = 'binary/octet-stream'
    return mime_type


def upload(aws_config, toupload):
    import boto3
    from botocore.exceptions import ClientError

    bucket_name = aws_config['bucket_name']
    aws_access_key_id = aws_config['aws_access_key_id']
    aws_secret_access_key = aws_config['aws_secret_access_key']
    # aws_root_path = aws_config['path']
    aws_path_by_value = aws_config['path_by_value']

    s3 = boto3.resource("s3",
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)

    uploaded = []
    for rpath, realfile in toupload.items():

        sha256hex = compute_sha256hex(realfile)
        copy_to_cache(realfile, sha256hex)

        # path_by_value
        object_key = os.path.join(aws_path_by_value, 'sha256', sha256hex)

        # object_key = os.path.join(aws_root_path, rpath)

        size = os.stat(realfile).st_size
        mime_type = guess_mime_type(realfile)

        aws_object = s3.Object(bucket_name, object_key)
        try:
            aws_object.load()
            # elogger.info('Object %s already exists' % rpath)
            status = 'known'
            elogger.info('%15s %8s  %s' % (status, friendly_size(size), rpath))

        except ClientError as e:
            not_found = e.response['Error']['Code'] == '404'
            if not_found:
                status = 'uploading'
                elogger.info('%15s %8s  %s' % (status, friendly_size(size), rpath))
                aws_object.upload_file(realfile, ExtraArgs={'ContentType': mime_type})

            else:
                raise
        url = 'http://%s.s3.amazonaws.com/%s' % (bucket_name, object_key)
        storage = dict(s3=dict(object_key=object_key, bucket_name=bucket_name, url=url))
        uploaded.append(dict(size=size, mime_type=mime_type, rpath=rpath, sha256hex=sha256hex, storage=storage))

    return uploaded


def object_exists(s3, bucket, key):
    from botocore.exceptions import ClientError
    try:
        h = s3.head_object(Bucket=bucket, Key=key)
        # print h
    except ClientError as e:
        return int(e.response['Error']['Code']) != 404
    return True


def compute_sha256hex(filename) -> str:
    cmd = ['shasum', '-a', '256', filename]
    res: bytes = subprocess.check_output(cmd)
    res2 = res.decode('utf-8')
    tokens = res2.split()
    h = tokens[0]
    assert len(h) == len('08c1fe03d3a6ef7dbfaccc04613ca561b11b5fd7e9d66b643436eb611dfba348')
    return h


def create_index_files(wd, job_id):
    for root, dirnames, filenames in os.walk(wd, followlinks=True):
        print(root, dirnames, filenames)
        index = os.path.join(root, 'index.html')
        if not os.path.exists(index):
            with open(index, 'w') as f:
                f.write(create_index(root, dirnames, filenames, job_id))


def create_index(root, dirnames, filenames, job_id):
    s = "<html><head></head><body>\n"

    url = DEFAULT_DTSERVER + '/humans/jobs/%s' % job_id
    s += '<p>These are the output for <a href="%s">Job %s</a>' % (url, job_id)
    s += '<table>'

    for d in dirnames:
        s += '\n<tr><td></td><td><a href="%s">%s/</td></tr>' % (d, d)

    for f in filenames:
        size = os.stat(os.path.join(root, f)).st_size
        s += '\n<tr><td>%.3f MB</td><td><a href="%s">%s</td></tr>' % (size / (1024 * 1024.0), f, f)

    s += '\n</table>'
    s += '\n</body></head>'
    return s
