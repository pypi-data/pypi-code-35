
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

import logging

from pentagon_datadog.rodd import Rodd


class Downtimes(Rodd):

    def add(self, destination, overwrite=False):
        self.template_file_name = 'downtime.tf.jinja'
        self._item_type = 'downtimes'
        logging.debug("Generating downtime .tf files")
        Rodd.add(self, destination, overwrite=True)
        self._validate_tf(destination)
