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


'''Server resources (API endpoints)'''


import os
import glob
import shutil
import subprocess

import simplejson

from flask import request
from flask_restful import Resource

import logging
logger = logging.getLogger(__name__)

from . import utils

from beat.core.dock import Host
from beat.core.environments import enumerate_packages

def make_error(status_code, message):
    """Overrides flask-restful's response handling to return a custom error message
    Adapted from https://stackoverflow.com/a/21639552

    Parameters:

        status_code (int): The HTTP status code to return

        message (str): The error message text to return
    """
    response = simplejson.dumps({
        'status': status_code,
        'message': message
    })
    response.status_code = status_code
    return response

class Layout(Resource):
    """Exposes toolchain layout functionality"""

    def __init__(self, config):
        self.config = config

    def post(self):
        data = request.get_json()
        if data != None and 'toolchain' in data:
            from beat.core.toolchain import Toolchain
            obj = Toolchain(self.config.path, data['toolchain'])
            diagram = obj.dot_diagram(is_layout=True)
            diagram.format = 'json'
            return diagram.pipe().decode()

        else:
            raise RuntimeError('Invalid post content for tc layout!')


class Environments(Resource):
    """Exposes local environment info"""

    def get(self):
        """Uses beat.core to get the local environment (docker) information
        and returns a list of environments"""
        host = Host(raise_on_errors=False)
        envs = host.processing_environments
        for env in envs.keys():
            envs[env]['queues'] = {}
            try:
                envs[env]['packages'] = enumerate_packages(host, env)
            except:
                envs[env]['packages'] = []
        return envs


class Templates(Resource):
    """Endpoint for generating template files"""
    def __init__(self, config):
        self.config = config

    def post(self):
        data = request.get_json()
        entity = data.pop('entity')
        name = data.pop('name')
        confirm = data.pop('confirm')
        utils.generate_python_template(entity, name, confirm, self.config, **data)


class Settings(Resource):
    """Exposes the prefix"""
    def __init__(self, config):
        self.config = config

    def get(self):
        """Uses beat.cmdline to get the prefix"""
        return { 'prefix': self.config.path }


def path_to_dict(path):
    """Generates a dict of the given file/folder in the BEAT prefix"""

    d = dict(name=os.path.basename(path))
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path, x))
                         for x in os.listdir(path)]
    elif os.path.isfile(path):
        d['type'] = "file"
        fname, fext = os.path.splitext(path)
        if fext == '.json':
            with open(path, 'rt') as f:
                d['json'] = simplejson.loads(f.read())
    return d


VALID_ENTITIES = [
    'dataformats',
    'databases',
    'libraries',
    'algorithms',
    'toolchains',
    'experiments',
    'plotters',
    'plotterparameters',
]
"""List of valid BEAT object entitities"""


def assert_valid_entity(v):
    """Asserts the passed value corresponds to a valid BEAT entity"""

    assert v in VALID_ENTITIES, '%s is not a valid BEAT entity ' \
        '(valid values are %s)' % (v, ', '.join(VALID_ENTITIES))


def generate_file_tree(entity, config):
    """Generates a file tree (of dicts) given a specific BEAT entity"""

    assert_valid_entity(entity)
    resource_path = os.path.join(config.path, entity)
    if not os.path.isdir(resource_path):
        raise IOError('Invalid resource path %s' % resource_path)

    return path_to_dict(resource_path)


def generate_json_entity(fto, parent_names):
    """Generates info for a file in the BEAT path"""
    if fto['type'] != 'file':
        raise Exception('bad file tree obj')

    fname, fext = os.path.splitext(fto['name'])

    name_str = ''
    for name in parent_names:
        name_str += name + '/'

    name_str += fname

    return {
        'name': name_str,
        'contents': fto['json']
    }


def generate_entity_tree(entity, config):
    """Generates the entire tree for an entity type from the prefix"""

    file_tree = generate_file_tree(entity, config)
    entity_tree = {}
    user_and_name = [
        'dataformats',
        'libraries',
        'algorithms',
        'toolchains',
        'plotters',
        'plotterparameters',
    ]

    if entity in user_and_name:
        for user in file_tree['children']:
            entity_tree[user['name']] = {}
            for obj in user['children']:
                entity_tree[user['name']][obj['name']] = list()
                for f in obj['children']:
                    fname, fext = os.path.splitext(f['name'])
                    if fext != '.json':
                        continue
                    parent_names = [user['name'], obj['name']]
                    json_obj = generate_json_entity(f, parent_names)
                    entity_tree[user['name']][obj['name']].append(json_obj)

    elif entity == 'databases':
        for obj in file_tree['children']:
            entity_tree[obj['name']] = list()
            for f in obj['children']:
                fname, fext = os.path.splitext(f['name'])
                if fext != '.json':
                    continue
                parent_names = [obj['name']]
                json_obj = generate_json_entity(f, parent_names)
                entity_tree[obj['name']].append(json_obj)

    elif entity == 'experiments':
        for user in file_tree['children']:
            uname = user['name']
            entity_tree[uname] = {}
            for tc_user in user['children']:
                tcuname = tc_user['name']
                entity_tree[uname][tcuname] = {}
                for tc_name in tc_user['children']:
                    tcname = tc_name['name']
                    entity_tree[uname][tcuname][tcname] = {}
                    for tc_version in tc_name['children']:
                        tcv = tc_version['name']
                        entity_tree[uname][tcuname][tcname][tcv] = list()
                        for exp_name in tc_version['children']:
                            fname, fext = os.path.splitext(exp_name['name'])
                            if fext != '.json':
                                continue
                            parent_names = [uname, tcuname, tcname, tcv]
                            json_obj = generate_json_entity(
                                exp_name, parent_names)
                            entity_tree[uname][tcuname][tcname][tcv].append(
                                json_obj)

    return entity_tree


def write_json(config, entity, obj, mode, copy_obj_name=''):
    """Writes JSON from a webapp request to the prefix using the specified
    mode"""

    assert_valid_entity(entity)
    resource_path = os.path.join(config.path, entity)
    name = obj['name']
    name_segs = name.split('/')
    contents = obj['contents']
    stringified = simplejson.dumps(contents, indent=4, sort_keys=True)

    folder_path = os.path.join(resource_path, '/'.join(name_segs[:-1]))
    file_subpath = os.path.join(resource_path, name)
    file_path = file_subpath + '.json'

    if mode == 'update':
        os.makedirs(folder_path, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(stringified)

    elif mode == 'create':
        if not os.path.isfile(file_path):
            os.makedirs(folder_path, exist_ok=True)
            if copy_obj_name != '':
                copy_obj_path = os.path.join(resource_path, copy_obj_name)
                if os.path.isfile(copy_obj_path + '.json'):
                    files_to_copy = glob.glob('%s.*' % copy_obj_path)
                    copy_locations = ['%s%s' % (file_subpath, os.path.splitext(f)[1]) for f in files_to_copy]
                    for i in range(0, len(files_to_copy)):
                        if files_to_copy[i].endswith('.json'): continue
                        shutil.copy(files_to_copy[i], copy_locations[i])
            with open(file_path, 'w') as f:
                f.write(stringified)

    elif mode == 'delete':
        if os.path.isfile(file_path):
            files_to_delete = glob.glob('%s.*' % file_subpath)
            for f in files_to_delete:
                os.remove(f)
            # taken from https://stackoverflow.com/a/23488980

            def remove_empty_dirs(path):
                """Remove empty directories recursively"""

                for root, dirnames, filenames in os.walk(path, topdown=False):
                    for dirname in dirnames:
                        remove_empty_dirs(
                            os.path.realpath(
                                os.path.join(root, dirname)
                            )
                        )
                    if not os.listdir(path): os.rmdir(path)

            remove_empty_dirs(folder_path)

    else:
        raise ValueError('Invalid write-mode `%s\'' % mode)


def gen_endpoint(entity):
    """Generates an endpoint for the given BEAT entity

    Exposes actions to perform on the prefix

    """

    class Endpoint(Resource):
        """A class representing the template for an endpoint for a BEAT entity"""

        def __init__(self, config):
            self.config = config

        def refresh(self):
            """Regenerates the entity tree"""
            try:
                return generate_entity_tree(entity, self.config)
            except IOError:
                return []

        def get(self):
            """Returns the entity tree"""
            return self.refresh()

        def post(self):
            """Creates a new object"""
            obj_list = request.get_json()
            if not isinstance(obj_list, list):
                obj_list = [obj_list]
            for o in obj_list:
                # two fields:
                # - "obj" field (the object to create)
                # - "copyObjName" field (the object that was copied, blank if
                #   not copied)
                obj = o['obj']
                copy_obj_name = o['copiedObjName']
                write_json(self.config, entity, obj, 'create', copy_obj_name)
            return self.refresh()

        def put(self):
            """Updates an already-existing object"""
            obj_list = request.get_json()
            if not isinstance(obj_list, list):
                obj_list = [obj_list]
            for obj in obj_list:
                write_json(self.config, entity, obj, 'update')
            return self.refresh()

        def delete(self):
            """Deletes an object"""
            obj = request.get_json()
            write_json(self.config, entity, obj, 'delete')
            return self.refresh()

    Endpoint.__name__ = entity

    return Endpoint
