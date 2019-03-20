
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

import unittest
import hashlib
import os
import logging

from pentagon_datadog.dashboard import Dashboards
from pentagon_datadog.monitor import Monitors
from pentagon_datadog.downtime import Downtimes
import oyaml as yaml


class TestDashboards(unittest.TestCase):
    name = "test-dashboards"
    test_input_file = "test/files/test_input.yml"

    def setUp(self):
        with open(self.test_input_file) as f:
            self._data = yaml.load(f.read())

        ds = Dashboards(self._data)
        ds.add("./", overwrite=True)
        pass

    def test_dashboard_output(self):
        gold = hashlib.md5(open("test/files/reactiveops_kubernetes_resource_timeboard.tf").read()).hexdigest()
        new = hashlib.md5(open("./reactiveops_kubernetes_resource_timeboard.tf").read()).hexdigest()

        logging.debug(gold)
        logging.debug(new)

        self.assertEqual(gold, new)

    def tearDown(self):
        os.remove("reactiveops_kubernetes_resource_timeboard.tf")


class TestMonitorDefinitionsGlobal(unittest.TestCase):
    name = "test-monitors"
    test_input_file = "test/files/test_input.yml"

    def setUp(self):
        with open(self.test_input_file) as f:
            self._data = yaml.load(f.read())
            self._data['definitions']['pods_pending_critical_threshold'] = 1234
        ms = Monitors(self._data)
        ms.add("./", overwrite=True)

    def test_pods_monitor_output(self):
        gold = hashlib.md5(open("test/files/test_pods_are_stuck_pending_def_global.tf").read()).hexdigest()
        new = hashlib.md5(open("test_pods_are_stuck_pending.tf").read()).hexdigest()

        logging.debug(gold)
        logging.debug(new)

        self.assertEqual(gold, new)

    def tearDown(self):
        os.remove("test_pods_are_stuck_pending.tf")


class TestMonitors(unittest.TestCase):
    name = "test-monitors"
    test_input_file = "test/files/test_input.yml"

    def setUp(self):
        self.deploy_replica_alert_namespaces = ['one', 'two', 'three']
        with open(self.test_input_file) as f:
            self._data = yaml.load(f.read())
        ms = Monitors(self._data)
        ms.add("./", overwrite=True)

    def test_pods_monitor_output(self):
        gold = hashlib.md5(open("test/files/test_pods_are_stuck_pending.tf").read()).hexdigest()
        new = hashlib.md5(open("test_pods_are_stuck_pending.tf").read()).hexdigest()

        logging.debug(gold)
        logging.debug(new)

        self.assertEqual(gold, new)

    def test_increase_in_network_errors(self):
        gold = hashlib.md5(open("test/files/test_increase_in_network_errors.tf").read()).hexdigest()
        new = hashlib.md5(open("test_increase_in_network_errors.tf").read()).hexdigest()

        logging.debug(gold)
        logging.debug(new)

        self.assertEqual(gold, new)

    def test_deployment_replica_alert(self):
        for namespace in self.deploy_replica_alert_namespaces:
            gold = hashlib.md5(open("test/files/test_deployment_replica_alert_{}.tf".format(namespace)).read()).hexdigest()
            new = hashlib.md5(open("test_deployment_replica_alert_{}.tf".format(namespace)).read()).hexdigest()

            logging.debug(gold)
            logging.debug(new)

            self.assertEqual(gold, new)

    def test_inline_definition_replacement(self):
        for namespace in self.deploy_replica_alert_namespaces:
            gold = hashlib.md5(open("test/files/test_var_replacement_for_inline_monitors.tf".format(namespace)).read()).hexdigest()
            new = hashlib.md5(open("test_var_replacement_for_inline_monitors.tf".format(namespace)).read()).hexdigest()

            logging.debug(gold)
            logging.debug(new)

            self.assertEqual(gold, new)

    def tearDown(self):
        os.remove("test_pods_are_stuck_pending.tf")
        os.remove("test_increase_in_network_errors.tf")
        os.remove("test_var_replacement_for_inline_monitors.tf")
        for namespace in self.deploy_replica_alert_namespaces:
            os.remove("test_deployment_replica_alert_{}.tf".format(namespace))


class TestDowntimes(unittest.TestCase):
    name = "test-downtimes"
    test_input_file = "test/files/test_input.yml"

    def setUp(self):
        with open(self.test_input_file) as f:
            self._data = yaml.load(f.read())
        ms = Downtimes(self._data)
        ms.add("./", overwrite=True)

    def test_downtime_output(self):
        gold = hashlib.md5(open("test/files/test_maintenance_window.tf").read()).hexdigest()
        new =hashlib.md5(open("test_maintenance_window.tf").read()).hexdigest()

        logging.debug(gold)
        logging.debug(new)

        self.assertEqual(gold, new)

    def tearDown(self):
        os.remove("test_maintenance_window.tf")
