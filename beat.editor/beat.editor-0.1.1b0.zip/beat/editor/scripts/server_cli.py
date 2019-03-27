#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#                                                                             #
# Copyright (c) 2016 Idiap Research Institute, http://www.idiap.ch/           #
# Contact: beat.support@idiap.ch                                              #
#                                                                             #
# This file is part of the beat.editor module of the BEAT platform.           #
#                                                                             #
# Commercial License Usage                                                    #
# Licensees holding valid commercial BEAT licenses may use this file in       #
# accordance with the terms contained in a written agreement between you      #
# and Idiap. For further information contact tto@idiap.ch                     #
#                                                                             #
# Alternatively, this file may be used under the terms of the GNU Affero      #
# Public License version 3 as published by the Free Software and appearing    #
# in the file LICENSE.AGPL included in the packaging of this file.            #
# The BEAT platform is distributed in the hope that it will be useful, but    #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY  #
# or FITNESS FOR A PARTICULAR PURPOSE.                                        #
#                                                                             #
# You should have received a copy of the GNU Affero Public License along      #
# with the BEAT platform. If not, see http://www.gnu.org/licenses/.           #
#                                                                             #
###############################################################################


"""The main entry for beat.editor (click-based) scripts.
"""


import os
import sys
import click
import pkg_resources
from click_plugins import with_plugins
from beat.cmdline.click_helper import AliasedGroup
from beat.cmdline.decorators import verbosity_option
from beat.cmdline.decorators import raise_on_error
from beat.cmdline.config import Configuration

EPILOG = '''\b
Example:
        $ beat editor serve
        $ beat editor serve --dev

        To run the development server add option --dev
        '''

@with_plugins(pkg_resources.iter_entry_points('beat.editor.cli'))
@click.group(cls=AliasedGroup)
@click.pass_context
def editor(ctx):
    """beat.editor commands webserver."""
    pass

@editor.command(epilog=EPILOG)
@click.option('--dev', help='Use the development version, which doesn\'t open a new web browser tab.',
             is_flag=True)
@click.option('--debug', '-d', help='Use the debug version of the javascript source to lauch the editor',
             is_flag=True)
@click.option('--prefix', '-p', help='Overrides the prefix of your local data. If not set use the value from your RC file [default: %(prefix)s]',
             type=click.STRING)
@click.option('--cache', '-c', help='Overrides the cache prefix. If not set, use the value from your RC file, otherwise defaults to `<prefix>/%(cache)s\'',
             type=click.STRING)
@click.option('--port', help='Overrides the port that the beat.editor server will listen on. By default will listen on port 5000.',
             default=5000,
             type=click.INT)
@verbosity_option()
@click.pass_context
@raise_on_error
def serve(ctx, dev, debug, prefix, cache, port):
    '''Run Flask server

    To run the development server add option --dev

      $ beat editor serve --dev
    '''

    ctx.meta['dev'] = dev
    ctx.meta['debug'] = debug
    ctx.meta['prefix'] = prefix
    ctx.meta['cache'] = cache

    completions = dict(
        prog=os.path.basename(sys.argv[0]),
        version=pkg_resources.require('beat.editor')[0].version
    )

    from beat.cmdline.config import Configuration
    completions.update(Configuration({}).as_dict())

    # Check that we are in a BEAT working folder
    from ..utils import setup_logger
    logger = setup_logger('beat.editor', ctx.meta['verbosity'])

    config = Configuration(ctx.meta)
    logger.info('BEAT prefix set to `%s\'', config.path)
    logger.info('BEAT cache set to `%s\'', config.cache)

    from flask import Flask, request, redirect, url_for
    from flask_restful import Api
    from flask_cors import CORS
    from ..resources import Layout, Templates, Environments, Settings
    from ..resources import VALID_ENTITIES, gen_endpoint

    static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../js')
    app = Flask(__name__, static_folder=static_folder, static_url_path='')
    errors = errors = {
        'PythonFileAlreadyExistsError': {
            'message': "The python template file trying to be created already exists.",
            'status': 409,
        }
    }
    api = Api(app, errors=errors)
    CORS(app)

    @app.route('/')
    def home():
        return redirect(url_for('static', filename='index.html'))

    api.add_resource(Layout, '/layout', resource_class_kwargs={'config': config})
    api.add_resource(Templates, '/templates', resource_class_kwargs={'config': config})
    api.add_resource(Settings, '/settings', resource_class_kwargs={'config': config})
    api.add_resource(Environments, '/environments')
    for entity in VALID_ENTITIES:
        api.add_resource(gen_endpoint(entity), '/' + entity,
                         resource_class_kwargs={'config': config})

    if not dev:
        import webbrowser
        webbrowser.open('http://localhost:{}'.format(port))

    return app.run(debug=debug, port=port)
