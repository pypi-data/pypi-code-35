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


import io
import os
import sys
import click
import logging
import simplejson
import collections

from PIL import Image

from beat.core import plotter
from beat.core import dataformat

from . import common
from .dataformats import pull_impl as dataformats_pull
from .plotterparameters import pull_impl as plotterparameters_pull
from .libraries import pull_impl as libraries_pull
from .decorators import raise_on_error
from .click_helper import AliasedGroup


logger = logging.getLogger(__name__)


def pull_impl(webapi, prefix, names, force, indentation, format_cache):
    """Copies plotters from the server.

    Parameters:

      webapi (object): An instance of our WebAPI class, prepared to access the
        BEAT server of interest

      prefix (str): A string representing the root of the path in which the
        user objects are stored

      names (:py:class:`list`): A list of strings, each representing the unique relative
        path of the objects to retrieve or a list of usernames from which to
        retrieve objects. If the list is empty, then we pull all available
        objects of a given type. If no user is set, then pull all public
        objects of a given type.

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

    # download required plotter
    status, names = common.pull(webapi, prefix, 'plotter', names,
                                ['declaration', 'code'], force,
                                indentation)

    # check dataformat, libraries, default plotterparameter used by plotter
    dataformats = []
    libraries = []
    for name in names:
        data = common.fetch_object(webapi, 'plotter', name, ['declaration', 'uses'])
        data = simplejson.loads(data['declaration'], object_pairs_hook=collections.OrderedDict)
        libraries_json = simplejson.loads(simplejson.dumps(data['uses']))
        for key, val in libraries_json.items():
            libraries.append(val)

        lb_status = libraries_pull(webapi, prefix, libraries, force,
                                     indentation + 2, format_cache)
        dataformats.append(data['dataformat'])
        # downloads any formats to which we depend on
        df_status = dataformats_pull(webapi, prefix, dataformats, force,
                                     indentation + 2, format_cache)

        # download default plotterparameter
        defaultplotters = common.fetch_object(webapi, 'defaultplotter', None, ['parameter'])
        for df in defaultplotters:
            if name == df['plotter']:
                plp_status = plotterparameters_pull(webapi, prefix, [df['parameter']], ['data', 'short_description', 'plotter'], force, indentation + 2)
    code = status + lb_status + df_status
    return code

def plot_impl(webapi, prefix, names, show, force, need_data_sample, inputdata, outputimage, plotterparameter, indentation, format_cache):
    """plot sample plot from the server.

    Parameters:

      webapi (object): An instance of our WebAPI class, prepared to access the
        BEAT server of interest

      prefix (str): A string representing the root of the path in which the
        user objects are stored

      names (:py:class:`list`): A list of strings, each representing the unique relative
        path of the objects to retrieve or a list of usernames from which to
        retrieve objects. If the list is empty, then we pull all available
        objects of a given type. If no user is set, then pull all public
        objects of a given type.

      need_data_sample (bool): If set to ``True``, then fetch sample data
        for plotter.

      force (bool): If set to ``True``, then overwrites local changes with the
        remotely retrieved copies.

      inputdata (str): The path to the json file containing data to
        be plotted.

      outputimage (str): The png filename for dumping the plot. If not set
        the default value is "output_image.png".

      plotterparameter (str): The name of the plotterparameter (without ".json"
        extension).

      indentation (int): The indentation level, useful if this function is
        called recursively while downloading different object types. This is
        normally set to ``0`` (zero).


    Returns:

      int: Indicating the exit status of the command, to be reported back to
        the calling process. This value should be zero if everything works OK,
        otherwise, different than zero (POSIX compliance).

    """

    indent = indentation * ' '
    name = names[0]

    # create a core_plotter
    core_plotter = plotter.Plotter(prefix, name)

    if not core_plotter.valid:
        message = 'Plotter %s is invalid' % core_plotter.name
        print(message)
        sys.exit()

    sample_data = None
    # get sample data
    if need_data_sample:
        sample_data = common.fetch_object(webapi, 'plotter', name, ['sample_data'])
        sample_data =  simplejson.loads(sample_data['sample_data'])

    # provide data
    if inputdata is None and not need_data_sample:
        message = 'Error: Missing --sample_data argument or inputdata'
        print(message)
        sys.exit()
    elif inputdata is not None:
        if type(inputdata) is str:
            with open(os.path.join(prefix, inputdata), 'r') as f:
                sample_data = simplejson.load(f)
            f.closed
        elif type(inputdata) is dict:
            sample_data = inputdata
        else:
            message = 'Error: inputdata should be dict or str type'
            print(message)
            sys.exit()

    # output
    plotter_path = os.path.join(prefix, common.TYPE_PLURAL['plotter'], name.rsplit('/', 1)[0])
    outputimage_name = "output_image.png"
    if outputimage is not None:
        outputimage_name = outputimage
    else:
        outputimage_name = os.path.join(plotter_path, outputimage_name)

    # plot
    corefmt = dataformat.DataFormat(prefix, core_plotter.dataformat.name)
    sample_data = corefmt.type().from_dict(sample_data, casting='unsafe')

    # plotterparameter
    data = None
    if plotterparameter is not None:
        try:
            with open(os.path.join(prefix, common.TYPE_NOSTORAGE['plotterparameter'], plotterparameter + '.json'), 'r') as f:
                data = simplejson.load(f, object_pairs_hook=collections.OrderedDict)
            f.closed
        except:
            logger.error("Error: unknown plotterparameter path")
    else:
        # download default plotterparameter
        defaultplotters = common.fetch_object(webapi, 'defaultplotter', None, ['parameter'])
        for df in defaultplotters:
            if name == df['plotter']:
                data = common.fetch_object(webapi, 'plotterparameter', df['parameter'], ['data'])

    if data is not None:
        to_remove = [key for key in data['data'].keys() if key not in core_plotter.parameters]
        for key in to_remove:
          del data['data'][key]

        data['data'].setdefault('content_type', 'image/png') #in case not set

        runnable = core_plotter.runner()
        runnable.setup(data['data'])
        assert runnable.ready
        data_to_plot = [('sample_plot', sample_data)]
        fig = runnable.process(data_to_plot)
        if show:
            im = Image.open(io.BytesIO(fig))
            im.show()
        output_name = os.path.join(prefix, outputimage_name)
        with open(output_name, "wb") as fh:
            fh.write(fig)
            logger.info("%ssaved image `%s'...", indent, output_name)
    else:
        logger.error("Error: data has not been set")
        return 1

    return 0



@click.group(cls=AliasedGroup)
@click.pass_context
def plotters(ctx):
    """Plotters commands"""
    pass



@plotters.command()
@click.option('--remote', help='Only acts on the remote copy of the list.',
              is_flag=True)
@click.pass_context
@raise_on_error
def list(ctx, remote):
    '''Lists all the plotters available on the platform.

    To list all existing plotters on your local prefix:

        $ beat plotters list
    '''
    if remote:
        with common.make_webapi(ctx.meta['config']) as webapi:
            return common.display_remote_list(webapi, 'plotter')
    else:
        return common.display_local_list(ctx.meta['config'].path, 'plotter')

@plotters.command()
@click.argument('names', nargs=-1)
@click.pass_context
@raise_on_error
def path(ctx, names):
  '''Displays local path of plotters files

  Example:
    $ beat plotters path xxx
  '''
  return common.display_local_path(ctx.meta['config'].path, 'plotter', names)


@plotters.command()
@click.argument('name', nargs=1)
@click.pass_context
@raise_on_error
def edit(ctx, name):
  '''Edit local plotter file

  Example:
    $ beat plotters edit xxx
  '''
  return common.edit_local_file(ctx.meta['config'].path,
                                ctx.meta['config'].editor, 'plotter',
                                name)


@plotters.command()
@click.argument('names', nargs=-1)
@click.pass_context
@raise_on_error
def check(ctx, names):
    '''Checks a local plotter for validity.

    $ beat plotters check xxx
    '''
    return common.check(ctx.meta['config'].path, 'plotter', names)



@plotters.command()
@click.argument('names', nargs=-1)
@click.option('--force', help='Performs operation regardless of conflicts',
              is_flag=True)
@click.pass_context
def pull(ctx, names, force):
    '''Downloads the specified plotters from the server.

       $ beat plotters pull xxx.
    '''
    with common.make_webapi(ctx.meta['config']) as webapi:
        name = common.make_up_remote_list(webapi, 'plotter', names)
        if name is None:
            return 1 #error
        return pull_impl(webapi, ctx.meta['config'].path, name, force, 0, {})



@plotters.command()
@click.argument('names', nargs=-1)
@click.option('--show', help='Show...',
              is_flag=True)
@click.option('--force', help='Performs operation regardless of conflicts',
              is_flag=True)
@click.option('--sample-data', help='Sample data...',
              is_flag=True)
@click.option('--input-data', help='<filename.json>',
              type=click.Path(exists=True))
@click.option('--output-image', help='<filename.png>')
@click.option('--plotter-parameter', help='<plotterparameter>')
@click.pass_context
@raise_on_error
def plot(ctx, names, show, force, sample_data, input_data, output_image,
         plotter_parameter):
    '''Plots an image.

       $ beat plotters plot [--show] [--force] [--sample_data]
       [--input-data=<filename.json>] [--output-image=<filename.png>]
       [--plotter-parameter=<plotterparameter>] [<name>]...
    '''
    with common.make_webapi(ctx.meta['config']) as webapi:
        return plot_impl(
            webapi, ctx.meta['config'].path, names, show, force, sample_data,
            input_data, output_image, plotter_parameter, 0, {}
        )



@plotters.command()
@click.argument('names', nargs=-1)
@click.pass_context
@raise_on_error
def create(ctx, names):
    '''Creates a new local plotter.

    $ beat plotters create xxx
    '''
    return common.create(ctx.meta['config'].path, 'plotter', names)



@plotters.command()
@click.argument('name', nargs=1)
@click.pass_context
@raise_on_error
def version(ctx, name):
    '''Creates a new version of an existing plotter.

    $ beat plotters version xxx
    '''
    return common.new_version(ctx.meta['config'].path, 'plotter', name)


@plotters.command()
@click.argument('src', nargs=1)
@click.argument('dst', nargs=1)
@click.pass_context
@raise_on_error
def fork(ctx, src, dst):
    '''Forks a local plotter.

    $ beat plotters fork xxx yyy
    '''
    return common.fork(ctx.meta['config'].path, 'plotter', src, dst)



@plotters.command()
@click.argument('names', nargs=-1)
@click.pass_context
@raise_on_error
def rm(ctx, names):
    '''Deletes a local plotter.

    $ beat plotters rm xxx
    '''
    return common.delete_local(ctx.meta['config'].path, 'plotter', names)
