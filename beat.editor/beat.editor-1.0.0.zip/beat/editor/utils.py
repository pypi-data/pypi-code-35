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


import os
import sys

import jinja2

import logging
logger = logging.getLogger(__name__)


ENV = jinja2.Environment(loader=jinja2.PackageLoader(__name__, 'templates'))
"""Jinja2 environment for loading our templates"""


def generate_database(views=None):
    """Generates a valid BEAT database from our stored template


    Parameters:

        views (:py:class:`list`, Optional): A list of strings that represents the
            views for the database


    Returns:

        str: The rendered template as a string

    """

    views = views or ['View']
    template = ENV.get_template('database.jinja2')
    return template.render(views=views)


def generate_library(uses=None):
    """Generates a valid BEAT library from our stored template


    Parameters:

        uses (:py:class:`dict`, Optional): A dict of other libraries that the
            library uses. Keys are the value to reference the library, values are
            the library being referenced.


    Returns:

        str: The rendered template as a string

    """

    uses = uses or {}
    template = ENV.get_template('library.jinja2')
    return template.render(uses=uses)


def generate_algorithm(contents):
    """Generates a valid BEAT algorithm from our stored template


    Parameters:

        contents (:py:class:`dict`): The algorithm's JSON metadata


    Returns:

        str: The rendered template as a string

    """

    template = ENV.get_template('algorithm.jinja2')
    return template.render(contents=contents)


def generate_plotter(uses):
    """Generates a valid BEAT plotter from our stored template


    Parameters:

        contents (:py:class:`dict`): The plotter's JSON metadata


    Returns:

        str: The rendered template as a string

    """

    uses = uses or {}
    template = ENV.get_template('plotter.jinja2')
    return template.render(uses=uses)


TEMPLATE_FUNCTION = dict(
    databases=generate_database,
    libraries=generate_library,
    algorithms=generate_algorithm,
    plotters=generate_plotter,
)

"""Functions for template instantiation within beat.editor"""

class PythonFileAlreadyExistsError(Exception):
    pass

def generate_python_template(entity, name, confirm, config, **kwargs):
    """Generates a template for a BEAT entity with the given named arguments


    Parameters:

        entity (str): A valid BEAT entity

        name (str): The name of the object to have a python file generated for

        confirm (:py:class:`boolean`): Whether to override the Python file if
            one is found at the desired location
    """

    resource_path = os.path.join(config.path, entity)
    file_path = os.path.join(resource_path, name) + '.py'
    if not confirm and os.path.isfile(file_path):
        # python file already exists
        raise PythonFileAlreadyExistsError

    s = TEMPLATE_FUNCTION[entity](**kwargs)

    with open(file_path, 'w') as f: f.write(s)

    return s


def setup_logger(name, verbosity):
    '''Sets up the logging of a script


    Parameters:

        name (str): The name of the logger to setup

        verbosity (int): The verbosity level to operate with. A value of ``0``
            (zero) means only errors, ``1``, errors and warnings; ``2``, errors,
            warnings and informational messages and, finally, ``3``, all types of
            messages including debugging ones.

    '''

    logger = logging.getLogger(name)
    formatter = logging.Formatter("%(name)s@%(asctime)s -- %(levelname)s: " \
                                  "%(message)s")

    _warn_err = logging.StreamHandler(sys.stderr)
    _warn_err.setFormatter(formatter)
    _warn_err.setLevel(logging.WARNING)

    class _InfoFilter:
        def filter(self, record): return record.levelno <= logging.INFO

    _debug_info = logging.StreamHandler(sys.stdout)
    _debug_info.setFormatter(formatter)
    _debug_info.setLevel(logging.DEBUG)
    _debug_info.addFilter(_InfoFilter())

    logger.addHandler(_debug_info)
    logger.addHandler(_warn_err)


    logger.setLevel(logging.ERROR)
    if verbosity == 1: logger.setLevel(logging.WARNING)
    elif verbosity == 2: logger.setLevel(logging.INFO)
    elif verbosity >= 3: logger.setLevel(logging.DEBUG)

    return logger
