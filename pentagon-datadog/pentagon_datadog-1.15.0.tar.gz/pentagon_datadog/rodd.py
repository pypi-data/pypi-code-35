
# Copyright 2018 ReactiveOps

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
import traceback
import glob
import re
import oyaml as yaml
import subprocess

from pentagon.component import ComponentBase

from pentagon.helpers import render_template, merge_dict


class Rodd(ComponentBase):
    _files_directory = os.path.dirname(__file__) + "/files/"

    def __init__(self, data, additional_args=None, **kwargs):
        self._defaults = {'options': {}}
        self._path = os.path.dirname(__file__)

        super(Rodd, self).__init__(data, additional_args, **kwargs)

        self._global_definitions = self._data.get('definitions', {})
        self._exceptions = self._data.get('exceptions', [])

    def _render_directory_templates(self, data):
        """ Overide Component method _render_directory_templates.
        Loop and use render_template helper method on all templates
        in destination directory, but use the _data['name'] as the base
        for the target file instead of the tempate name itself """

        # Here is where it differs from the Component._render_directory_templates()
        target_file_name = os.path.normpath("{}{}.tf".format(self._destination, data['resource_name']))

        render_template(self.template_file_name, self._files_directory, target_file_name, data, delete_template=False, overwrite=self._overwrite)

    def _flatten_options(self, data):
        """ If there is a options key in the _data, flatten it
        This makes transformation from datadog json easier """
        for key, value in data.get('options', {}).iteritems():
            data[key] = value
        return data

    def add(self, destination, overwrite=False):
        """ Build up a set of Rodd resources and then create a TF file for each. """

        self._destination = destination
        self._overwrite = overwrite

        processed_resources = {}

        if self._item_type not in self._data:
            raise Exception('No {} declared or no file argument passed'.format(self._item_type))
            return

        for resource in self._data[self._item_type]:
            source = resource.get('source')
            if source is None:
                self._create_tf_file(resource)
            else:
                item_local_paths = []
                if "." in source:
                    item_local_paths = ["{}/{}/{}.yml".format(self._path, self._item_type, ("/").join(source.split(".")))]
                else:
                    item_local_paths = glob.glob("{}/{}/{}/*.yml".format(self._path, self._item_type, source))
                logging.debug("{}: {}".format(self._item_type.title(), item_local_paths))

                for local_source_path in item_local_paths:
                    resource_data = {}
                    resource_id = '/'.join(local_source_path.split('/')[-3:])
                    logging.debug("Loading {}".format(local_source_path))
                    logging.debug("Source is: {} ".format(source))
                    logging.debug("Resource id is: {} ".format(resource_id))

                    if os.path.isfile(local_source_path) and ('/').join(local_source_path.split('/')[-2:]) in self.exceptions:
                        continue

                    with open(local_source_path, 'r') as item_file:
                        item_dict = yaml.load(item_file, Loader=yaml.loader.FullLoader)
                    # If the items are being pulled from a family,
                    # then use all the values in the default item
                    if len(item_local_paths) > 1:
                        resource_data = item_dict
                    else:
                        # Otherwise, overwrite the item values with
                        # the values being passed in
                        resource_data = merge_dict(resource, item_dict)

                    processed_resources[resource_id] = resource_data

                    logging.debug('Processed resource: {}'.format(resource_data))

        self._save_processed_resources(processed_resources)

    def _save_processed_resources(self, resources):
        """ Loop through dict of processed resources and generates tf file for each one. """
        for key, data in resources.iteritems():
            definitions = self.definitions(data)
            definition_namespace = definitions.get('namespace')

            # Create multiple tf files for resources that vary by namespace
            if data.get('vary_by_namespace'):
                if isinstance(definition_namespace, list):
                    for namespace in definition_namespace:
                        data_copy = data.copy()
                        if not data_copy.get('definitions'):
                            data_copy['definitions'] = {}
                        data_copy['definitions']['namespace'] = namespace
                        self._create_tf_file(data_copy)
                    continue

                if not definition_namespace:
                    logging.warning('Namespace value missing, required for {}'.format(key))
                    continue

            self._create_tf_file(data)

    def _create_tf_file(self, data):
        """ Create TF file for a single resource. """
        try:
            # transform item name
            data = self._replace_definitions(data)

            raw_resource_name = data.get('name', data.get('title', 'Unknown Title'))

            data['resource_name'] = re.sub('^_', '', re.sub('[^0-9a-zA-Z]+', '_', raw_resource_name.lower())).strip('_')
            logging.debug("New Name: {}".format(data['resource_name']))

            data = self._flatten_options(data)

            for key in data:
                if type(data[key]) in [unicode, str]:
                    data[key] = data[key].replace('"', '\\"')

            self._remove_init_file()
            self._render_directory_templates(data)

        except Exception as e:
            logging.error("Error occured configuring component")
            logging.error(e)
            logging.debug(traceback.format_exc(e))

    def _validate_tf(self, destination):
        """ Validate terraform in the path provided. """
        try:
            if len([file for file in os.listdir(destination) if os.path.isfile(file) and file.endswith(".tf")]) > 0:
                tf = subprocess.check_output(['terraform', 'fmt', destination])
                logging.debug("terraform fmt output:\n{}".format(tf))

                validate = subprocess.check_output(['terraform', 'validate', '--check-variables=false', destination])
        except subprocess.CalledProcessError as validateErr:
            logging.warning("Error validating terraform: {}".format(validateErr.output))

    def _replace_definitions(self, data):
        """ Replace ${definitions} with their value """

        def _replace_definition(string, definitions):
            if type(string) in [unicode, str]:
                for var, value in definitions.iteritems():
                    logging.debug("Replacing Definition: {}:{}".format(var, value))
                    string = string.replace("${%s}" % str(var), str(value))

            return string

        # Locally scopped copy of definitions to add monitor defaults to
        _definitions = self.definitions(data)

        logging.debug("Definitions: {}".format(_definitions))
        for key in data.keys():

            # Just handle the tags and thresholds separately since they are a list.  Probably a
            # better way to do this in the future
            if key == 'tags':
                logging.debug("Found tags: {}".format(data[key]))
                for index, item in enumerate(data[key]):
                    data[key][index] = _replace_definition(data[key][index], _definitions)
            elif key == 'thresholds':
                logging.debug("Found thresholds: {}".format(data[key]))
                for threshold_type in data[key]:
                    data[key][threshold_type] = _replace_definition(data[key][threshold_type], _definitions)
            else:
                data[key] = _replace_definition(data[key], _definitions)
        return data

    def definitions(self, data):
        """ Return dictionary of merged definitions: global, definition_defaults, definitions """
        definitions = merge_dict(data.get('definition_defaults', {}), self._global_definitions.copy(), clobber=True)
        definitions = merge_dict(definitions, data.get('definitions', {}), clobber=True)
        return definitions

    @property
    def exceptions(self):
        exception_paths = []
        for e in self._exceptions:
            exception_paths.append("{}.yml".format(e.replace('.', '/')))
        return exception_paths
