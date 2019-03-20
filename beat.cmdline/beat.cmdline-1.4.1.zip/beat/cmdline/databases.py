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
import click
import glob
import random
import zmq
import logging
import simplejson

from beat.core.hash import toPath
from beat.core.hash import hashDataset
from beat.core.utils import NumpyJSONEncoder
from beat.core.database import Database
from beat.core.data import RemoteDataSource
from beat.core import dock
from beat.core import inputs
from beat.core import utils

from . import common
from .decorators import raise_on_error
from .click_helper import AliasedGroup


logger = logging.getLogger(__name__)


CMD_DB_INDEX = 'index'
CMD_VIEW_OUTPUTS = 'databases_provider'


# ----------------------------------------------------------


def load_database_sets(configuration, database_name):
    # Process the name of the database
    parts = database_name.split('/')

    if len(parts) == 2:
        db_name = os.path.join(*parts[:2])
        protocol_filter = None
        set_filter = None

    elif len(parts) == 3:
        db_name = os.path.join(*parts[:2])
        protocol_filter = parts[2]
        set_filter = None

    elif len(parts) == 4:
        db_name = os.path.join(*parts[:2])
        protocol_filter = parts[2]
        set_filter = parts[3]

    else:
        logger.error("Database specification should have the format "
                     "`<database>/<version>/[<protocol>/[<set>]]', the value "
                     "you passed (%s) is not valid", database_name)
        return (None, None)

    # Load the dataformat
    dataformat_cache = {}
    database = Database(configuration.path,
                        db_name, dataformat_cache)
    if not database.valid:
        logger.error("Failed to load the database `%s':", db_name)
        for e in database.errors:
            logger.error('  * %s', e)
        return (None, None, None)

    # Filter the protocols
    protocols = database.protocol_names

    if protocol_filter is not None:
        if protocol_filter not in protocols:
            logger.error("The database `%s' does not have the protocol `%s' - "
                         "choose one of `%s'", db_name, protocol_filter,
                         ', '.join(protocols))

            return (None, None, None)

        protocols = [protocol_filter]

    # Filter the sets
    loaded_sets = []

    for protocol_name in protocols:
        sets = database.set_names(protocol_name)

        if set_filter is not None:
            if set_filter not in sets:
                logger.error("The database/protocol `%s/%s' does not have the "
                             "set `%s' - choose one of `%s'",
                             db_name, protocol_name, set_filter,
                             ', '.join(sets))
                return (None, None, None)

            sets = [z for z in sets if z == set_filter]

        loaded_sets.extend([(protocol_name, set_name,
                             database.set(protocol_name, set_name))
                            for set_name in sets])

    return (db_name, database, loaded_sets)


# ----------------------------------------------------------


def start_db_container(configuration, cmd, host,
                       db_name, protocol_name, set_name, database, db_set,
                       excluded_outputs=None, uid=None, db_root=None):

    input_list = inputs.InputList()

    input_group = inputs.InputGroup(set_name, restricted_access=False)
    input_list.add(input_group)

    db_configuration = {
        'inputs': {},
        'channel': set_name,
    }

    if uid is not None:
        db_configuration['datasets_uid'] = uid

    if db_root is not None:
        db_configuration['datasets_root_path'] = db_root

    for output_name, dataformat_name in db_set['outputs'].items():
        if excluded_outputs is not None and output_name in excluded_outputs:
            continue

        dataset_hash = hashDataset(db_name, protocol_name, set_name)
        db_configuration['inputs'][output_name] = dict(
            database=db_name,
            protocol=protocol_name,
            set=set_name,
            output=output_name,
            channel=set_name,
            hash=dataset_hash,
            path=toPath(dataset_hash, '.db')
        )

    db_tempdir = utils.temporary_directory()

    with open(os.path.join(db_tempdir, 'configuration.json'), 'wt') as f:
        simplejson.dump(db_configuration, f, indent=4)

    tmp_prefix = os.path.join(db_tempdir, 'prefix')
    if not os.path.exists(tmp_prefix):
        os.makedirs(tmp_prefix)

    database.export(tmp_prefix)

    if db_root is None:
        json_path = os.path.join(tmp_prefix, 'databases', db_name + '.json')

        with open(json_path, 'r') as f:
            db_data = simplejson.load(f)

        database_path = db_data['root_folder']
        db_data['root_folder'] = os.path.join('/databases', db_name)

        with open(json_path, 'w') as f:
            simplejson.dump(db_data, f, indent=4)

    try:
        db_envkey = host.db2docker([db_name])
    except:
        raise RuntimeError("No environment found for the database `%s' "
                           "- available environments are %s" % (
                               db_name,
                               ", ".join(host.db_environments.keys())))

    # Creation of the container
    # Note: we only support one databases image loaded at the same time
    CONTAINER_PREFIX = '/beat/prefix'
    CONTAINER_CACHE = '/beat/cache'

    database_port = random.randint(51000, 60000)
    if cmd == CMD_VIEW_OUTPUTS:
        db_cmd = [
            cmd,
            '0.0.0.0:{}'.format(database_port),
            CONTAINER_PREFIX,
            CONTAINER_CACHE
        ]
    else:
        db_cmd = [
            cmd,
            CONTAINER_PREFIX,
            CONTAINER_CACHE,
            db_name,
            protocol_name,
            set_name
        ]

    databases_container = host.create_container(db_envkey, db_cmd)
    databases_container.uid = uid

    if cmd == CMD_VIEW_OUTPUTS:
        databases_container.add_port(
            database_port, database_port, host_address=host.ip)
        databases_container.add_volume(db_tempdir, '/beat/prefix')
        databases_container.add_volume(configuration.cache, '/beat/cache')
    else:
        databases_container.add_volume(tmp_prefix, '/beat/prefix')
        databases_container.add_volume(configuration.cache, '/beat/cache', read_only=False)

    # Specify the volumes to mount inside the container
    if 'datasets_root_path' not in db_configuration:
        databases_container.add_volume(
            database_path, os.path.join('/databases', db_name))
    else:
        databases_container.add_volume(db_configuration['datasets_root_path'],
                                       db_configuration['datasets_root_path'])

    # Start the container
    host.start(databases_container)

    if cmd == CMD_VIEW_OUTPUTS:
        # Communicate with container
        zmq_context = zmq.Context()
        db_socket = zmq_context.socket(zmq.PAIR)
        db_address = 'tcp://{}:{}'.format(host.ip, database_port)
        db_socket.connect(db_address)

        for output_name, dataformat_name in db_set['outputs'].items():
            if excluded_outputs is not None and \
               output_name in excluded_outputs:
                continue

            data_source = RemoteDataSource()
            data_source.setup(db_socket, output_name,
                              dataformat_name, configuration.path)

            input_ = inputs.Input(output_name,
                                  database.dataformats[dataformat_name],
                                  data_source)
            input_group.add(input_)

        return (databases_container, db_socket, zmq_context, input_list)

    return databases_container


# ----------------------------------------------------------


def pull_impl(webapi, prefix, names, force, indentation, format_cache):
    """Copies databases (and required dataformats) from the server.

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

      format_cache (dict): A dictionary containing all dataformats already
        downloaded.


    Returns:

      int: Indicating the exit status of the command, to be reported back to
        the calling process. This value should be zero if everything works OK,
        otherwise, different than zero (POSIX compliance).

    """

    from .dataformats import pull_impl as dataformats_pull

    status, names = common.pull(webapi, prefix, 'database', names,
                                ['declaration', 'code', 'description'],
                                force, indentation)

    # see what dataformats one needs to pull
    dataformats = []
    for name in names:
        obj = Database(prefix, name)
        dataformats.extend(obj.dataformats.keys())

    # downloads any formats to which we depend on
    df_status = dataformats_pull(webapi, prefix, dataformats, force,
                                 indentation + 2, format_cache)

    return status + df_status


# ----------------------------------------------------------


def index_outputs(configuration, names, uid=None, db_root=None, docker=False):

    names = common.make_up_local_list(configuration.path, 'database', names)
    retcode = 0

    if docker:
        host = dock.Host(raise_on_errors=False)

    for database_name in names:
        logger.info("Indexing database %s...", database_name)

        (db_name, database, sets) = load_database_sets(
            configuration, database_name)
        if database is None:
            retcode += 1
            continue

        for protocol_name, set_name, db_set in sets:
            if not docker:
                try:
                    view = database.view(protocol_name, set_name)
                except SyntaxError as error:
                    logger.error("Failed to load the database `%s':",
                                 database_name)
                    logger.error('  * Syntax error: %s', error)
                    view = None

                if view is None:
                    retcode += 1
                    continue

                dataset_hash = hashDataset(db_name, protocol_name, set_name)
                try:
                    view.index(os.path.join(configuration.cache,
                                            toPath(dataset_hash, '.db')))
                except RuntimeError as error:
                  logger.error("Failed to load the database `%s':",
                               database_name)
                  logger.error('  * Runtime error %s', error)
                  retcode += 1
                  continue

            else:
                databases_container = \
                    start_db_container(configuration, CMD_DB_INDEX,
                                       host, db_name, protocol_name, set_name,
                                       database, db_set,
                                       uid=uid, db_root=db_root
                                       )
                status = host.wait(databases_container)
                logs = host.logs(databases_container)
                host.rm(databases_container)

                if status != 0:
                    logger.error("Error occurred: %s", logs)
                    retcode += 1

    return retcode


# ----------------------------------------------------------


def list_index_files(configuration, names):

    names = common.make_up_local_list(configuration.path, 'database', names)

    retcode = 0

    for database_name in names:
        logger.info("Listing database %s indexes...", database_name)

        (db_name, database, sets) = load_database_sets(
            configuration, database_name)
        if database is None:
            retcode += 1
            continue

        for protocol_name, set_name, db_set in sets:
            dataset_hash = hashDataset(db_name, protocol_name, set_name)
            index_filename = toPath(dataset_hash)
            basename = os.path.splitext(index_filename)[0]
            for g in glob.glob(basename + '.*'):
                logger.info(g)

    return retcode


# ----------------------------------------------------------


def delete_index_files(configuration, names):

    names = common.make_up_local_list(configuration.path, 'database', names)

    retcode = 0

    for database_name in names:
        logger.info("Deleting database %s indexes...", database_name)

        (db_name, database, sets) = load_database_sets(
            configuration, database_name)
        if database is None:
            retcode += 1
            continue

        for protocol_name, set_name, db_set in sets:
            for output_name in db_set['outputs'].keys():
                dataset_hash = hashDataset(db_name, protocol_name, set_name)
                index_filename = toPath(dataset_hash)
                basename = os.path.join(configuration.cache,
                                        os.path.splitext(index_filename)[0])

                for g in glob.glob(basename + '.*'):
                    logger.info("removing `%s'...", g)
                    os.unlink(g)

                common.recursive_rmdir_if_empty(os.path.dirname(basename),
                                                configuration.cache)

    return retcode


# ----------------------------------------------------------


def view_outputs(configuration, dataset_name, excluded_outputs=None, uid=None,
                 db_root=None, docker=False):

    def data_to_json(data, indent):
        value = common.stringify(data.as_dict())

        value = simplejson.dumps(value, indent=4, cls=NumpyJSONEncoder) \
            .replace('"BEAT_LIST_DELIMITER[', '[') \
            .replace(']BEAT_LIST_DELIMITER"', ']') \
            .replace('"...",', '...') \
            .replace('"BEAT_LIST_SIZE(', '(') \
            .replace(')BEAT_LIST_SIZE"', ')')

        return ('\n' + ' ' * indent).join(value.split('\n'))

    # Load the infos about the database set
    (db_name, database, sets) = load_database_sets(configuration, dataset_name)
    if (database is None) or (len(sets) != 1):
        return 1

    (protocol_name, set_name, db_set) = sets[0]

    if excluded_outputs is not None:
        excluded_outputs = map(lambda x: x.strip(),
                               excluded_outputs.split(','))

    # Setup the view so the outputs can be used
    if not docker:
        view = database.view(protocol_name, set_name)

        if view is None:
            return 1

        dataset_hash = hashDataset(db_name, protocol_name, set_name)
        view.setup(os.path.join(configuration.cache,
                                toPath(dataset_hash, '.db')), pack=False)
        input_group = inputs.InputGroup(set_name, restricted_access=False)

        for output_name, dataformat_name in db_set['outputs'].items():
            if excluded_outputs is not None and \
               output_name in excluded_outputs:
                continue

            input = inputs.Input(output_name,
                                 database.dataformats[dataformat_name],
                                 view.data_sources[output_name])
            input_group.add(input)

    else:
        host = dock.Host(raise_on_errors=False)

        (databases_container, db_socket, zmq_context, input_list) = \
            start_db_container(configuration, CMD_VIEW_OUTPUTS,
                               host, db_name, protocol_name,
                               set_name, database, db_set,
                               excluded_outputs=excluded_outputs,
                               uid=uid, db_root=db_root)

        input_group = input_list.group(set_name)

    retvalue = 0

    # Display the data
    try:
        previous_start = -1

        while input_group.hasMoreData():
            input_group.next()

            start = input_group.data_index
            end = input_group.data_index_end

            if start != previous_start:
                print(80 * '-')

                print('FROM %d TO %d' % (start, end))

                whole_inputs = [input_ for input_ in input_group
                                if input_.data_index == start and
                                input_.data_index_end == end]

                for input in whole_inputs:
                    label = ' - ' + str(input.name) + ': '
                    print(label + data_to_json(input.data, len(label)))

                previous_start = start

            selected_inputs = \
                [input_ for input_ in input_group
                 if input_.data_index == input_group.first_data_index and
                 (input_.data_index != start or
                  input_.data_index_end != end)]

            grouped_inputs = {}
            for input_ in selected_inputs:
                key = (input_.data_index, input_.data_index_end)
                if key not in grouped_inputs:
                    grouped_inputs[key] = []
                grouped_inputs[key].append(input)

            sorted_keys = sorted(grouped_inputs.keys())

            for key in sorted_keys:
                print
                print('  FROM %d TO %d' % key)

                for input in grouped_inputs[key]:
                    label = '   - ' + str(input.name) + ': '
                    print(label + data_to_json(input.data, len(label)))

    except Exception as e:
        logger.error("Failed to retrieve the next data: %s", e)
        retvalue = 1

    if docker:
        host.kill(databases_container)
        status = host.wait(databases_container)
        logs = host.logs(databases_container)
        host.rm(databases_container)
        if status != 0:
            logger.error("Docker error: %s", logs)


    return retvalue


# ----------------------------------------------------------


@click.group(cls=AliasedGroup)
@click.pass_context
def databases(ctx):
    """Database commands"""
    pass


@databases.command()
@click.option('--remote', help='Only acts on the remote copy of the database.',
              is_flag=True)
@click.pass_context
@raise_on_error
def list(ctx, remote):
    '''Lists all the databases available on the platform.

    To list all existing databases on your local prefix:

        $ beat databases list
    '''
    configuration = ctx.meta['config']
    if remote:
        with common.make_webapi(configuration) as webapi:
            return common.display_remote_list(webapi, 'database')
    else:
        return common.display_local_list(configuration.path, 'database')


@databases.command()
@click.argument('names', nargs=-1)
@click.pass_context
@raise_on_error
def path(ctx, names):
  '''Displays local path of databases files

  Example:
    $ beat databases path xxx
  '''
  return common.display_local_path(ctx.meta['config'].path, 'database', names)


@databases.command()
@click.argument('name', nargs=1)
@click.pass_context
@raise_on_error
def edit(ctx, name):
  '''Edit local database file

  Example:
    $ beat databases edit xxx
  '''
  return common.edit_local_file(ctx.meta['config'].path,
                                ctx.meta['config'].editor, 'database',
                                name)



@databases.command()
@click.argument('db_names', nargs=-1)
@click.pass_context
@raise_on_error
def check(ctx, db_names):
    '''Checks a local database for validity.

    $ beat databases check [<name>]...

    <name>:
        Database name formatted as "<database>/<version>"
    '''
    return common.check(ctx.meta['config'].path, 'database', db_names)


@databases.command()
@click.argument('db_names', nargs=-1)
@click.option('--force', help='Performs operation regardless of conflicts',
              is_flag=True)
@click.pass_context
@raise_on_error
def pull(ctx, db_names, force):
    '''Downloads the specified databases from the server.

       $ beat databases pull [<name>]...

    <name>:
        Database name formatted as "<database>/<version>"
    '''
    configuration = ctx.meta['config']
    with common.make_webapi(configuration) as webapi:
        return pull_impl(webapi, configuration.path, db_names, force, 0, {})


@databases.command()
@click.argument('db_names', nargs=-1)
@click.option('--force', help='Performs operation regardless of conflicts',
              is_flag=True)
@click.option('--dry-run', help='Dry run',
              is_flag=True)
@click.pass_context
@raise_on_error
def push(ctx, db_names, force, dry_run):
    '''Uploads databases to the server (must provide a valid admin token).

    $ beat databases push [<name>]...

    <name>:
        Database name formatted as "<database>/<version>"

    '''
    configuration = ctx.meta['config']
    with common.make_webapi(configuration) as webapi:
        return common.push(webapi, configuration.path, 'database',
                           db_names, ['name', 'declaration',
                                      'code', 'description'],
                           {}, force, dry_run, 0)


@databases.command()
@click.argument('db_names', nargs=-1)
@click.pass_context
@raise_on_error
def diff(ctx, db_names):
    '''Shows changes between the local database and the remote version.

    $ beat databases diff [<name>]...

    <name>:
        Database name formatted as "<database>/<version>"
    '''
    configuration = ctx.meta['config']
    if len(db_names) < 1:
        raise click.ClickException("Requires at least one database name")
    with common.make_webapi(configuration) as webapi:
        return common.diff(webapi, configuration.path, 'database',
                           db_names[0],
                           ['declaration', 'code', 'description'])


@databases.command()
@click.pass_context
@raise_on_error
def status(ctx):
    '''Shows (editing) status for all available databases'''
    configuration = ctx.meta['config']
    with common.make_webapi(configuration) as webapi:
        return common.status(webapi, configuration.path, 'database')[0]


@databases.command()
@click.argument('db_names', nargs=-1)
@click.pass_context
@raise_on_error
def version(ctx, db_names):
    '''Creates a new version of an existing database.

    $ beat databases version [<name>]...

    <name>:
        Database name formatted as "<database>/<version>"

    '''
    configuration = ctx.meta['config']
    if len(db_names) < 1:
        raise click.ClickException("Requires at least one database name")
    return common.new_version(configuration.path, 'database', db_names[0])


@databases.command()
@click.argument('db_names', nargs=-1)
@click.option('--list', help='List index files matching output if they exist',
              is_flag=True)
@click.option('--delete', help='Delete index files matching output if they '
              'exist (also, recursively deletes empty directories)',
              is_flag=True)
@click.option('--checksum', help='Checksums index files', is_flag=True,
              default=True)
@click.option('--uid', type=click.INT, default=None)
@click.option('--db-root', help="Database root")
@click.option('--docker', is_flag=True)
@click.pass_context
@raise_on_error
def index(ctx, db_names, list, delete, checksum, uid, db_root, docker):
    '''Indexes all outputs (of all sets) of a database.

    To index the contents of a database

        $ beat databases index simple/1

    To index the contents of a protocol on a database

        $ beat databases index simple/1/double

    To index the contents of a set in a protocol on a database

        $ beat databases index simple/1/double/double
    '''
    configuration = ctx.meta['config']
    code = 1
    if list:
        code = list_index_files(configuration, db_names)
    elif delete:
        code = delete_index_files(configuration, db_names)
    elif checksum:
        code = index_outputs(configuration, db_names, uid=uid,
                             db_root=db_root, docker=docker)
    return code

@databases.command()
@click.argument('set_name', nargs=1)
@click.option('--exclude', help='When viewing, excludes this output',
              default=None)
@click.option('--uid', type=click.INT, default=None)
@click.option('--db-root', help="Database root")
@click.option('--docker', is_flag=True)
@click.pass_context
@raise_on_error
def view(ctx, set_name, exclude, uid, db_root, docker):
    '''View the data of the specified dataset.

    To view the contents of a specific set

    $ beat databases view simple/1/protocol/set
    '''
    configuration = ctx.meta['config']
    if exclude is not None:
        return view_outputs(
            configuration, set_name, exclude, uid=uid, db_root=db_root,
            docker=docker)
    return view_outputs(
        configuration, set_name, uid=uid, db_root=db_root, docker=docker
    )
