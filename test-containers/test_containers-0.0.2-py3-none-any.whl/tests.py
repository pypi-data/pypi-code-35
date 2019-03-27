from test_containers.utils import execute_command
import docker
import os
import shutil
import sys
import tempfile
import time
import unittest

docker_client = docker.from_env()


class ContainerTest:
    def __init__(self, container, test):
        self.container = container
        self.test = test
        self.container_name = self.container["name"].replace("-", "_")
        self.test_name = self.test["name"].replace("-", "_").replace(" ", "_")
        self.test_case_object = None
        self.test_result = None

    def __evaluate_result(self):
        if "exit-code" in self.test:
            self.test_case_object.assertEqual(self.test["exit-code"], self.test_result["exit-code"])

        if "expected-output" in self.test:
            self.test_case_object.assertRegexpMatches(self.test_result["output"], self.test["expected-output"])

        if "excluded-output" in self.test:
            self.test_case_object.assertNotRegexpMatches(self.test_result["output"], self.test["excluded-output"])

        if "expected-error" in self.test:
            self.test_case_object.assertRegexpMatches(self.test_result["error"], self.test["expected-error"])

        if "excluded-error" in self.test:
            self.test_case_object.assertNotRegexpMatches(self.test_result["error"], self.test["excluded-error"])

        if "files" in self.test:
            for file_tests in self.test["files"]:
                if "exists" in file_tests:
                    self.test_case_object.assertEqual(os.path.exists(file_tests["path"]), file_tests["exists"])
                if "expected-content" in file_tests or "excluded-content" in file_tests:
                    with open(file_tests["path"]) as f:
                        file_content = f.read()
                    if "expected-content" in file_tests:
                        self.test_case_object.assertRegexpMatches(file_content, file_tests["expected-content"])
                    if "excluded-content" in file_tests:
                        self.test_case_object.assertNotRegexpMatches(file_content, file_tests["excluded-content"])

    def __expand_environment_variables(self):
        if "environment-variables" not in self.test:
            return

        environment_variables = self.test["environment-variables"]
        for variable, definition in environment_variables.items():
            environment_variables[variable] = execute_command(definition)["output"]

        for key in ["command", "expected-output", "excluded-output", "expected-error", "excluded-error"]:
            if key not in self.test:
                continue
            for variable, value in environment_variables.items():
                self.test[key] = self.test[key].replace("${%s}" % variable, value)

    def run_test(self, test_case_object):
        self.test_case_object = test_case_object
        with ContainerTestEnvironment(container=self.container):
            self.__expand_environment_variables()
            self.test_result = execute_command(self.test["command"])
            self.__evaluate_result()


class ContainerTestCase(unittest.TestCase):
    def setUp(self):
        self.previous_working_dir = os.getcwd()
        self.working_dir = tempfile.mkdtemp()
        os.chdir(self.working_dir)

    def tearDown(self):
        os.chdir(self.previous_working_dir)
        shutil.rmtree(self.working_dir)

    @staticmethod
    def generate_tests(tests):
        def generate_test_method(test):
            def generated_test_method(self):
                test.run_test(self)
            return generated_test_method

        for test in tests:
            test_name = "test_%s_%s" % (test.container_name, test.test_name)
            setattr(ContainerTestCase, test_name, generate_test_method(test))


class ContainerTestEnvironment:
    def __init__(self, container):
        self.container = container

    def __enter__(self):
        self.docker_container = docker_client.containers.run(self.container["name"], detach=True,
                                                             **self.container["arguments"])
        self.__wait_container_ready()

    def __exit__(self, type, value, traceback):
        self.docker_container.stop()

    def __wait_container_ready(self):
        inspection = docker_client.api.inspect_container(self.docker_container.id)
        if "Health" in inspection["State"]:
            print("\nWaiting for container to be healthy... ", end="", file=sys.stderr, flush=True)
            while inspection["State"]["Health"]["Status"] != "healthy":
                time.sleep(2)
                inspection = docker_client.api.inspect_container(self.docker_container.id)
            print("Container healthy.", file=sys.stderr)
        else:
            time.sleep(2)
