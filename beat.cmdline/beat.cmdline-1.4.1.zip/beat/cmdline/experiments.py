#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###################################################################################
#                                                                                 #
# Copyright (c) 2019 Idiap Research Institute, http://www.idiap.ch/               #
# Contact: beat.support@idiap.ch                                                  #
#                                                                                 #
# Redistribution and use in source and binary forms, with or without              #
# modification, are permitted provided that the following conditions are met:     #
#                                                                                 #
# 1. Redistributions of source code must retain the above copyright notice, this  #
# list of conditions and the following disclaimer.                                #
#                                                                                 #
# 2. Redistributions in binary form must reproduce the above copyright notice,    #
# this list of conditions and the following disclaimer in the documentation       #
# and/or other materials provided with the distribution.                          #
#                                                                                 #
# 3. Neither the name of the copyright holder nor the names of its contributors   #
# may be used to endorse or promote products derived from this software without   #
# specific prior written permission.                                              #
#                                                                                 #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND #
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED   #
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE          #
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE    #
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL      #
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR      #
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER      #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,   #
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE   #
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.            #
#                                                                                 #
###################################################################################


import os
import logging
import glob
import click
import oset
import simplejson

from beat.core.experiment import Experiment
from beat.core.execution import DockerExecutor
from beat.core.execution import LocalExecutor
from beat.core.utils import NumpyJSONEncoder
from beat.core.data import CachedDataSource, load_data_index
from beat.core.dock import Host
from beat.core.hash import toPath
from beat.core.hash import hashDataset

from . import common
from .plotters import plot_impl as plotters_plot
from .plotters import pull_impl as plotters_pull
from .decorators import raise_on_error
from .click_helper import AliasedGroup


logger = logging.getLogger(__name__)


def run_experiment(configuration, name, force, use_docker, use_local, quiet):
    '''Run experiments locally'''

    def load_result(executor):
        '''Loads the result of an experiment, in a single go'''

        f = CachedDataSource()
        assert f.setup(os.path.join(executor.cache,
                                    executor.data['result']['path'] + '.data'),
                       executor.prefix)
        data, start, end = f[0]
        return data

    def print_results(executor):
        data = load_result(executor)
        r = reindent(simplejson.dumps(data.as_dict(), indent=2,
                                          cls=NumpyJSONEncoder), 2)
        logger.info("  Results:\n%s", r)

    def reindent(s, n):
        '''Re-indents output so it is more visible'''
        margin = n * ' '
        return margin + ('\n' + margin).join(s.split('\n'))

    def simplify_time(s):
        '''Re-writes the time so it is easier to understand it'''

        minute = 60.0
        hour = 60 * minute
        day = 24 * hour

        if s <= minute:
            return "%.2f s" % s
        elif s <= hour:
            minutes = s // minute
            seconds = s - (minute * minutes)
            return "%d m %.2f s" % (minutes, seconds)
        elif s <= day:
            hours = s // hour
            minutes = (s - (hour * hours)) // minute
            seconds = s - (hour * hours + minute * minutes)
            return "%d h %d m %.2f s" % (hours, minutes, seconds)
        else:
            days = s // day
            hours = (s - (day * days)) // hour
            minutes = (s - (day * days + hour * hours)) // minute
            seconds = s - (day * days + hour * hours + minute * minutes)
            return "%d days %d h %d m %.2f s" % (days, hours, minutes, seconds)

    def simplify_size(s):
        '''Re-writes the size so it is easier to understand it'''

        kb = 1024.0
        mb = kb * kb
        gb = kb * mb
        tb = kb * gb

        if s <= kb:
            return "%d bytes" % s
        elif s <= mb:
            return "%.2f kilobytes" % (s / kb)
        elif s <= gb:
            return "%.2f megabytes" % (s / mb)
        elif s <= tb:
            return "%.2f gigabytes" % (s / gb)
        return "%.2f terabytes" % (s / tb)

    def index_experiment_databases(cache_path, experiment):
        for block_name, infos in experiment.datasets.items():
            view = infos['database'].view(infos['protocol'], infos['set'])
            filename = toPath(hashDataset(infos['database'].name,
                                          infos['protocol'],
                                          infos['set']),
                              suffix='.db')
            database_index_path = os.path.join(cache_path, filename)
            if not os.path.exists(database_index_path):
                logger.info("Index for database %s not found, building it", infos['database'].name)
                view.index(database_index_path)

    dataformat_cache = {}
    database_cache = {}
    algorithm_cache = {}
    library_cache = {}

    experiment = Experiment(configuration.path, name,
                            dataformat_cache, database_cache,
                            algorithm_cache, library_cache)

    if not experiment.valid:
        logger.error("Failed to load the experiment `%s':", name)
        for e in experiment.errors:
            logger.error('  * %s', e)
        return 1

    if not os.path.exists(configuration.cache):
        os.makedirs(configuration.cache)
        logger.info("Created cache path `%s'", configuration.cache)

    index_experiment_databases(configuration.cache, experiment)

    scheduled = experiment.setup()

    if use_docker:
        # load existing environments
        host = Host(raise_on_errors=False)

    # can we execute it?
    for key, value in scheduled.items():

        # checks and sets-up executable
        executable = None  # use the default

        if use_docker:
            env = value['configuration']['environment']
            search_key = '%s (%s)' % (env['name'], env['version'])
            if search_key not in host:
                logger.error("Cannot execute block `%s' on environment `%s': "
                             "environment was not found' - please install it",
                             key, search_key)
                return 1

        if use_docker:
            executor = DockerExecutor(host, configuration.path,
                                      value['configuration'],
                                      configuration.cache, dataformat_cache,
                                      database_cache, algorithm_cache,
                                      library_cache)
        else:
            executor = LocalExecutor(configuration.path,
                                     value['configuration'],
                                     configuration.cache, dataformat_cache,
                                     database_cache, algorithm_cache,
                                     library_cache,
                                     configuration.database_paths)

        if not executor.valid:
            logger.error(
                "Failed to load the execution information for `%s':", key)
            for e in executor.errors:
                logger.error('  * %s', e)
            return 1

        if executor.outputs_exist and not force:
            logger.info("Skipping execution of `%s' for block `%s' "
                        "- outputs exist", executor.algorithm.name, key)
            if executor.analysis and not quiet:
                logger.extra("  Outputs produced:")
                print_results(executor)
            continue

        logger.info("Running `%s' for block `%s'",
                    executor.algorithm.name, key)
        if executable is not None:
            logger.extra("  -> using executable at `%s'", executable)
        else:
            logger.extra("  -> using fallback (default) environment")

        with executor:
            result = executor.process()

        if result['status'] != 0:
            logger.error("Block did not execute properly - outputs were reset")
            logger.error("  Standard output:\n%s",
                         reindent(result['stdout'], 4))
            logger.error("  Standard error:\n%s",
                         reindent(result['stderr'], 4))
            logger.error("  Captured user error:\n%s",
                         reindent(result['user_error'], 4))
            logger.error("  Captured system error:\n%s",
                         reindent(result['system_error'], 4))
            logger.extra("  Environment: %s" % 'default environment')
            return 1
        elif use_docker:
            stats = result['statistics']
            cpu_stats = stats['cpu']
            data_stats = stats['data']

            cpu_total = cpu_stats['total']
            # Likely means that GPU was used
            if not cpu_total:
                cpu_total = 1.0

            logger.extra("  CPU time (user, system, total, percent): "
                         "%s, %s, %s, %d%%",
                         simplify_time(cpu_stats['user']),
                         simplify_time(cpu_stats['system']),
                         simplify_time(cpu_total),
                         100. * (cpu_stats['user'] + cpu_stats['system']) /
                         cpu_total)
            logger.extra("  Memory usage: %s",
                         simplify_size(stats['memory']['rss']))
            logger.extra("  Cached input read: %s, %s",
                         simplify_time(data_stats['time']['read']),
                         simplify_size(data_stats['volume']['read']))
            logger.extra("  Cached output write: %s, %s",
                         simplify_time(data_stats['time']['write']),
                         simplify_size(data_stats['volume']['write']))
            logger.extra("  Communication time: %s (%d%%)",
                         simplify_time(data_stats['network']['wait_time']),
                         100. * data_stats['network']['wait_time'] /
                         cpu_total)
        else:
            logger.extra("  Environment: %s" % 'local environment')

        if not quiet:
            if executor.analysis:
                print_results(executor)

            logger.extra("  Outputs produced:")
            if executor.analysis:
                logger.extra("    * %s", executor.data['result']['path'])
            else:
                for name, details in executor.data['outputs'].items():
                    logger.extra("    * %s", details['path'])
        else:
            logger.info("Done")

    return 0


def caches_impl(configuration, name, ls, delete, checksum):
    '''List all cache files involved in this experiment'''

    dataformat_cache = {}
    database_cache = {}
    algorithm_cache = {}
    library_cache = {}

    experiment = Experiment(configuration.path, name,
                            dataformat_cache, database_cache,
                            algorithm_cache, library_cache)

    if not experiment.valid:
        logger.error("Failed to load the experiment `%s':", name)
        for e in experiment.errors:
            logger.error('  * %s', e)
        return 1

    scheduled = experiment.setup()

    block_list = []
    for key, value in scheduled.items():
        block = {
            'name': key,
            'algorithm': value['configuration']['algorithm'],
            'is_analyser': False,
            'paths': []
        }

        if 'outputs' in value['configuration']:  # normal block
            for name, data in value['configuration']['outputs'].items():
                block['paths'].append(data['path'])
        else:  # analyzer
            block['is_analyser'] = True
            block['paths'].append(value['configuration']['result']['path'])

        block_list.append(block)

    for block in block_list:
        block_type = 'analyzer' if block['is_analyser'] else 'algorithm'
        logger.info("block: `%s'", block['name'])
        logger.info("  %s: `%s'", block_type, block['algorithm'])

        for path in block['paths']:
            # prefix cache path
            path = os.path.join(configuration.cache, path)
            logger.info("  output: `%s'", path)

            if ls:
                for file in glob.glob(path + '.*'):
                    logger.info('    %s' % file)

            if delete:
                for file in glob.glob(path + '.*'):
                    logger.info("removing `%s'...", file)
                    os.unlink(file)

                common.recursive_rmdir_if_empty(
                    os.path.dirname(path), configuration.cache)

            if checksum:
                assert load_data_index(configuration.cache, path + '.data')
                logger.info("index for `%s' can be loaded and checksums", path)

    return 0


def pull_impl(webapi, prefix, names, force, indentation, format_cache):
    """Copies experiments (and required toolchains/algorithms) from the server.

    Parameters:

      webapi (object): An instance of our WebAPI class, prepared to access the
        BEAT server of interest

      prefix (str): A string representing the root of the path in which the
        user objects are stored

      names (:py:class:`list`): A list of strings, each representing the unique
        relative path of the objects to retrieve or a list of usernames from
        which to retrieve objects. If the list is empty, then we pull all
        available objects of a given type. If no user is set, then pull all
        public objects of a given type.

      force (bool): If set to ``True``, then overwrites local changes with the
        remotely retrieved copies.

      indentation (int): The indentation level, useful if this function is
        called recursively while downloading different object types. This is
        normally set to ``0`` (zero).


    Returns:

      int: Indicating the exit status of the command, to be reported back to
        the calling process. This value should be zero if everything works OK,
        otherwise, different than zero (POSIX compliance).

    """

    from .algorithms import pull_impl as algorithms_pull
    from .databases import pull_impl as databases_pull

    status, names = common.pull(webapi, prefix, 'experiment', names,
                                ['declaration', 'description'], force,
                                indentation)

    if status != 0:
        logger.error(
            "could not find any matching experiments - widen your search")
        return status

    # see what dataformats one needs to pull
    databases = oset.oset()
    toolchains = oset.oset()
    algorithms = oset.oset()
    for name in names:
        try:
            obj = Experiment(prefix, name)
            if obj.toolchain:
                toolchains.add(obj.toolchain.name)
            databases |= obj.databases.keys()
            algorithms |= obj.algorithms.keys()

        except Exception as e:
            logger.error("loading `%s': %s...", name, str(e))

    # downloads any formats to which we depend on
    format_cache = {}
    library_cache = {}
    tc_status, _ = common.pull(webapi, prefix, 'toolchain',
                               toolchains, ['declaration', 'description'],
                               force, indentation + 2)
    db_status = databases_pull(webapi, prefix, databases, force,
                               indentation + 2, format_cache)
    algo_status = algorithms_pull(webapi, prefix, algorithms, force,
                                  indentation + 2, format_cache, library_cache)

    return status + tc_status + db_status + algo_status


def plot_impl(webapi, configuration, prefix, names, remote_results, show, force, indentation, format_cache, outputfolder=None):
    """Plots experiments from the server.

    Parameters:

      webapi (object): An instance of our WebAPI class, prepared to access the
        BEAT server of interest

      configuration (object): An instance of the configuration, to access the
        BEAT server and current configuration for information

      prefix (str): A string representing the root of the path in which the
        user objects are stored

      names (:py:class:`list`): A list of strings, each representing the unique relative
        path of the objects to retrieve or a list of usernames from which to
        retrieve objects. If the list is empty, then we pull all available
        objects of a given type. If no user is set, then pull all public
        objects of a given type.

      remote_results(bool): If set to ``True``, then fetch results data
        for the experiments from the server.

      force (bool): If set to ``True``, then overwrites local changes with the
        remotely retrieved copies.

      indentation (int): The indentation level, useful if this function is
        called recursively while downloading different object types. This is
        normally set to ``0`` (zero).

      outputfolder (str): A string representing the path in which the
        experiments plot will be stored

    Returns:

      int: Indicating the exit status of the command, to be reported back to
        the calling process. This value should be zero if everything works OK,
        otherwise, different than zero (POSIX compliance).

    """

    status = 0
    RESULTS_SIMPLE_TYPE_NAMES  = ('int32', 'float32', 'bool', 'string')

    if remote_results:
        if outputfolder is None:
            output_folder = configuration.path
        else:
            # check if directory exists else create
            if not os.path.isdir(outputfolder):
                os.mkdir(os.path.join(configuration.path, outputfolder))
            output_folder = os.path.join(configuration.path, outputfolder)

    for name in names:
        if not remote_results:
            if outputfolder is None:
                output_folder = os.path.join(configuration.path, common.TYPE_PLURAL['experiment'], name.rsplit('/', 1)[0])
            else:
                # check if directory exists else create
                if not os.path.isdir(outputfolder):
                    os.mkdir(os.path.join(configuration.path, outputfolder))
                output_folder = os.path.join(configuration.path, outputfolder)

        check_plottable = False
        if not os.path.exists(configuration.cache) or remote_results:
            experiment  = simplejson.loads(simplejson.dumps(common.fetch_object(webapi, "experiment", name, ['results'])))
            results = experiment['results']['analysis']
            for key, value in results.iteritems():
                # remove non plottable results
                if value['type'] not in RESULTS_SIMPLE_TYPE_NAMES:
                    output_name = name.rsplit('/', 1)[1] + '_' + key + '.png'
                    output_name = os.path.join(output_folder, output_name)
                    pl_status = plotters_pull(webapi, configuration.path, [value['type']], force, indentation + 2, {})
                    plot_status = plotters_plot(webapi, configuration.path, [value['type']], show, False, False, value['value'],
                        output_name, None, indentation + 2, format_cache)
                    status += pl_status
                    status += plot_status
                    check_plottable = True
        else:
            # make sure experiment exists locally or pull it
            experiments = pull_impl(webapi, configuration.path, [name], force, indentation, format_cache)

            # get information from cache
            dataformat_cache = {}
            database_cache = {}
            algorithm_cache = {}
            library_cache = {}

            experiment = Experiment(configuration.path, name,
                                    dataformat_cache, database_cache,
                                    algorithm_cache, library_cache)


            scheduled = experiment.setup()
            for key, value in scheduled.items():
                executor = LocalExecutor(configuration.path,
                                         value['configuration'],
                                         configuration.cache, dataformat_cache,
                                         database_cache, algorithm_cache,
                                         library_cache,
                                         configuration.database_paths)

                if 'result' in executor.data:
                    f = CachedDataSource()
                    assert f.setup(os.path.join(executor.cache,
                                                executor.data['result']['path'] + '.data'),
                                   executor.prefix)
                    data, start, end = f[0]

                    for the_data in data.as_dict():
                        attr = getattr(data, the_data)
                        if attr.__class__.__name__.startswith('plot'):
                            datatype = attr.__class__.__name__.replace('_','/')
                            # remove non plottable results
                            if datatype not in RESULTS_SIMPLE_TYPE_NAMES:
                                output_name = name.rsplit('/', 1)[1] + '_' + the_data + '.png'
                                output_name = os.path.join(output_folder, output_name)
                                pl_status = plotters_pull(webapi, configuration.path, [datatype], force, indentation + 2, {})
                                plot_status = plotters_plot(webapi, configuration.path, [datatype], show, False, False,
                                    data.as_dict()[the_data], output_name, None, indentation + 2, format_cache)
                                status += pl_status
                                status += plot_status
                                check_plottable = True
        if not check_plottable:
            print('Experiments results are not plottable')

    return status


@click.group(cls=AliasedGroup)
@click.pass_context
def experiments(ctx):
    """experiments commands"""
    pass


@experiments.command()
@click.argument('name', nargs=1)
@click.option('--force', help='Performs operation regardless of conflicts',
              is_flag=True)
@click.option('--docker', help='Uses the docker executor to execute the '
              'experiment using docker containers',
              is_flag=True)
@click.option('--local', help='Uses the local executor to execute the '
              'experiment on the local machine (default)',
              default=True, is_flag=True)
@click.option('--quiet', help='Be less verbose',
              is_flag=True)
@click.pass_context
@raise_on_error
def run(ctx, name, force, docker, local, quiet):
    ''' Runs an experiment locally'''
    config = ctx.meta.get('config')
    return run_experiment(config, name, force, docker, local, quiet)


@experiments.command()
@click.argument('name', nargs=1)
@click.option('--list', help='List cache files matching output if they exist',
              is_flag=True)
@click.option('--delete', help='Delete cache files matching output if they '
              'exist (also, recursively deletes empty directories)',
              is_flag=True)
@click.option('--checksum', help='Checksums indexes for cache files',
              is_flag=True)
@click.pass_context
@raise_on_error
def caches(ctx, name, list, delete, checksum):
    '''Lists all cache files used by this experiment'''
    config = ctx.meta.get('config')
    return caches_impl(config, name, list, delete, checksum)


@experiments.command()
@click.option('--remote', help='Only acts on the remote copy of the list.',
              is_flag=True)
@click.pass_context
@raise_on_error
def list(ctx, remote):
    '''Lists all the experiments available on the platform.

    To list all existing experiments on your local prefix:

        $ beat experiments list
    '''
    config = ctx.meta.get('config')
    if remote:
        with common.make_webapi(config) as webapi:
            return common.display_remote_list(webapi, 'experiment')
    else:
        return common.display_local_list(config.path, 'experiment')


@experiments.command()
@click.argument('names', nargs=-1)
@click.pass_context
@raise_on_error
def path(ctx, names):
  '''Displays local path of experiment files

  Example:
    $ beat experiments path xxx
  '''
  return common.display_local_path(ctx.meta['config'].path, 'experiment', names)


@experiments.command()
@click.argument('name', nargs=1)
@click.pass_context
@raise_on_error
def edit(ctx, name):
  '''Edit local experiment file

  Example:
    $ beat experiments edit xxx
  '''
  return common.edit_local_file(ctx.meta['config'].path,
                                ctx.meta['config'].editor, 'experiment',
                                name)


@experiments.command()
@click.argument('names', nargs=-1)
@click.pass_context
@raise_on_error
def check(ctx, names):
    '''Checks a local experiment for validity.

    $ beat experiments check xxx
    '''
    config = ctx.meta.get('config')
    return common.check(config.path, 'experiment', names)


@experiments.command()
@click.argument('names', nargs=-1)
@click.option('--force', help='Performs operation regardless of conflicts',
              is_flag=True)
@click.pass_context
@raise_on_error
def pull(ctx, names, force):
    '''Downloads the specified experiments from the server.

       $ beat experiments pull xxx.
    '''
    config = ctx.meta.get('config')
    with common.make_webapi(config) as webapi:
        return pull_impl(webapi, config.path, names, force, 0, {})


@experiments.command()
@click.argument('names', nargs=-1)
@click.option('--force', help='Performs operation regardless of conflicts',
              is_flag=True)
@click.option('--dry-run', help="Doesn't really perform the task, just "
              "comments what would do", is_flag=True)
@click.pass_context
@raise_on_error
def push(ctx, names, force, dry_run):
    '''Uploads experiments to the server.

    Example:
      $ beat experiments push --dry-run yyy
    '''
    config = ctx.meta.get('config')
    with common.make_webapi(config) as webapi:
        return common.push(
            webapi, config.path, 'experiment', names,
            ['name', 'declaration', 'toolchain', 'description'],
            {}, force, dry_run, 0
        )


@experiments.command()
@click.argument('name', nargs=1)
@click.pass_context
@raise_on_error
def diff(ctx, name):
    '''Shows changes between the local dataformat and the remote version.

    Example:
      $ beat experiments diff xxx
    '''
    config = ctx.meta.get('config')
    with common.make_webapi(config) as webapi:
        return common.diff(
            webapi, config.path, 'experiment', name,
            ['declaration', 'description']
        )


@experiments.command()
@click.pass_context
@raise_on_error
def status(ctx):
    '''Shows (editing) status for all available experiments.

    Example:
      $ beat experiments status
    '''
    config = ctx.meta.get('config')
    with common.make_webapi(config) as webapi:
        return common.status(webapi, config.path, 'experiment')[0]


@experiments.command()
@click.argument('src', nargs=1)
@click.argument('dst', nargs=1)
@click.pass_context
@raise_on_error
def fork(ctx, src, dst):
    '''Forks a local experiment.

    $ beat experiments fork xxx yyy
    '''
    config = ctx.meta.get('config')
    return common.fork(config.path, 'experiment', src, dst)


@experiments.command()
@click.argument('names', nargs=-1)
@click.option('--remote', help='Only acts on the remote copy of the experiment',
              is_flag=True)
@click.pass_context
@raise_on_error
def rm(ctx, names, remote):
    '''Deletes a local experiment (unless --remote is specified).

    $ beat experiments rm xxx
    '''
    config = ctx.meta.get('config')
    if remote:
        with common.make_webapi(config) as webapi:
            return common.delete_remote(webapi, 'experiment', names)
    else:
        return common.delete_local(config.path, 'experiment', names)


@experiments.command()
@click.argument('names', nargs=-1)
@click.option('--path', help='Use path to write files to disk (instead of the '
              'current directory)', type=click.Path())
@click.pass_context
@raise_on_error
def draw(ctx, names, path):
    '''Creates a visual representation of the experiment.'''
    config = ctx.meta.get('config')
    return common.dot_diagram(config.path, 'experiment', names, path, [])


@experiments.command()
@click.argument('names', nargs=-1)
@click.option('--force', help='Performs operation regardless of conflicts',
              is_flag=True)
@click.option('--remote', help='Only acts on the remote copy of the experiment',
              is_flag=True)
@click.option('--show', help='Show...',
              is_flag=True)
@click.option('--output-folder', help='<folder>', type=click.Path(exists=True))
@click.pass_context
@raise_on_error
def plot(ctx, names, force, remote, show, output_folder):
    '''Plots output images of the experiment.'''
    config = ctx.meta.get('config')
    with common.make_webapi(config) as webapi:
        return plot_impl(
            webapi, config, 'experiment', names, remote, show, force, 0, {},
            output_folder
        )
