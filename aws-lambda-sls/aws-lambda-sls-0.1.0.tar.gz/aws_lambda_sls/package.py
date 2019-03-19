# -*- coding: utf-8 -*-
import os
import re
import sys
import hashlib
import datetime
import subprocess
import aws_lambda_sls.models as models
from fnmatch import fnmatch
from email.parser import FeedParser
from aws_lambda_sls.compat import lambda_abi
from aws_lambda_sls.compat import pip_import_string
from aws_lambda_sls.compat import pip_no_compile_c_env_vars
from aws_lambda_sls.compat import pip_no_compile_c_shim
from aws_lambda_sls.utils import serialize_to_json, OSUtils
from aws_lambda_sls import constants
from importreqs.importreqs import get_intersected_distributions
try:
    from pip.req import parse_requirements
    from pip.download import PipSession
except Exception as ex:
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession


class InvalidSourceDistributionNameError(Exception):
    pass


class MissingDependencyError(Exception):
    """Raised when some dependencies could not be packaged for any reason."""
    def __init__(self, missing):
        self.missing = missing


class NoSuchPackageError(Exception):
    """Raised when a package name or version could not be found."""
    def __init__(self, package_name):
        super(NoSuchPackageError, self).__init__(
            "Could not satisfy the requirement: %s" % package_name)


class PackageDownloadError(Exception):
    """Generic networking error during a package download."""
    pass


class LambdaDeploymentPackager(object):
    _VENDOR_DIR = "vendor"

    def __init__(self, app_object, osutils, dependency_builder, ui):
        self._app_object = app_object
        self._osutils = osutils
        self._dependency_builder = dependency_builder
        self._ui = ui

    @property
    def sys_include_path(self):
        return self._app_object.config.get("PACKAGE_INCLUDE_SYS_PATH") or []

    @property
    def ignore_include_file(self):
        return self._app_object.config.get("PACKAGE_INCLUDE_IGNORE_FILE") or []

    def _get_ignores_files(self, project_dir):
        ignore_file_path = self._osutils.joinpath(project_dir, ".gitignore")
        if os.path.exists(ignore_file_path):
            ignores_files = [i.strip("/\n") for i in open(ignore_file_path).readlines()]
        else:
            ignores_files = []
        ignores_files.append(self._VENDOR_DIR)
        ignores_files += [i.strip("/\n") for i in constants.GITIGNORE.split("\n")]
        return set(ignores_files) - set(self.ignore_include_file)

    def _get_requirements_filename(self, project_dir):
        requirements_file_path = self._osutils.joinpath(project_dir, "requirements.txt")
        return requirements_file_path

    def _is_ignore_file(self, file_name, ignore_files):
        return any(fnmatch(file_name, ignore) for ignore in ignore_files)

    def create_deployment_package(self, package_filename):
        self._ui.write("Ready to create deployment package.\n")
        project_dir = self._app_object.root_path
        requirements_file_path = self._get_requirements_filename(project_dir)
        with self._osutils.tempdir() as site_packages_dir:
            try:
                self._dependency_builder.build_site_packages(
                    requirements_file_path, site_packages_dir)
            except MissingDependencyError as e:
                missing_packages = "\n".join([p.identifier for p
                                              in e.missing])
                self._ui.write(
                    constants.MISSING_DEPENDENCIES_TEMPLATE % missing_packages)
            dirname = self._osutils.dirname(
                self._osutils.abspath(package_filename))
            if not self._osutils.directory_exists(dirname):
                self._osutils.makedirs(dirname)
            with self._osutils.open_zip(package_filename, "w",
                                        self._osutils.ZIP_DEFLATED) as z:
                self._add_py_deps(z, site_packages_dir)
                self._add_project_files(z, project_dir)
                self._add_vendor_files(z, self._osutils.joinpath(
                    project_dir, self._VENDOR_DIR))
                for sys_path in sys.path:
                    if os.path.basename(sys_path) in self.sys_include_path:
                        self._add_py_deps(z, sys_path)
        self._ui.write("Create deployment package success.\n")
        return package_filename

    def _add_vendor_files(self, zipped, dirname):
        if not self._osutils.directory_exists(dirname):
            return
        prefix_len = len(dirname) + 1
        for root, _, filenames in self._osutils.walk(dirname):
            for filename in filenames:
                full_path = self._osutils.joinpath(root, filename)
                zip_path = full_path[prefix_len:]
                zipped.write(full_path, zip_path)

    def _add_py_deps(self, zip_fileobj, deps_dir):
        prefix_len = len(deps_dir) + 1
        for root, dirnames, filenames in self._osutils.walk(deps_dir):
            for filename in filenames:
                full_path = self._osutils.joinpath(root, filename)
                zip_path = full_path[prefix_len:]
                zip_fileobj.write(full_path, zip_path)

    def _add_project_files(self, zip_fileobj, project_dir):
        ignore_files = self._get_ignores_files(project_dir)
        if self._osutils.directory_exists(project_dir):
            for rootdir, _, filenames in self._osutils.walk(project_dir):
                if self._is_ignore_file(os.path.basename(rootdir), ignore_files):
                    continue
                for filename in filenames:
                    if self._is_ignore_file(filename, ignore_files):
                        continue
                    fullpath = self._osutils.joinpath(rootdir, filename)
                    zip_path = fullpath[len(project_dir) + 1:]
                    zip_fileobj.write(fullpath, zip_path)

    def _hash_project_dir(self, requirements_filename, vendor_dir):
        if not self._osutils.file_exists(requirements_filename):
            contents = b''
        else:
            contents = self._osutils.get_file_contents(
                requirements_filename, binary=True)
        h = hashlib.md5(contents)
        if self._osutils.directory_exists(vendor_dir):
            self._hash_vendor_dir(vendor_dir, h)
        return h.hexdigest()

    def _hash_vendor_dir(self, vendor_dir, md5):
        for rootdir, _, filenames in self._osutils.walk(vendor_dir):
            for filename in filenames:
                fullpath = self._osutils.joinpath(rootdir, filename)
                with self._osutils.open(fullpath, "rb") as f:
                    for chunk in iter(lambda: f.read(1024 * 1024), b''):
                        md5.update(chunk)

    def inject_latest_app(self, deployment_package_filename, project_dir):
        self._ui.write("Regen deployment package.\n")
        tmpzip = deployment_package_filename + ".tmp.zip"

        with self._osutils.open_zip(deployment_package_filename, "r") as inzip:
            with self._osutils.open_zip(tmpzip, "w",
                                        self._osutils.ZIP_DEFLATED) as outzip:
                for el in inzip.infolist():
                    if self._needs_latest_version(el.filename):
                        continue
                    else:
                        contents = inzip.read(el.filename)
                        outzip.writestr(el, contents)
                self._add_project_files(outzip, project_dir)
        self._osutils.move(tmpzip, deployment_package_filename)

    def _needs_latest_version(self, filename):
        return filename == "app.py"


class PipDependencyBuilder(object):
    """Build site-packages by manually downloading and unpacking wheels.

    Pip is used to download all the dependency sdists. Then wheels that
    compatible with lambda are downloaded. Any source packages that do not
    have a matching wheel file are built into a wheel and that file is checked
    for compatibility with the lambda python runtime environment.

    All compatible wheels that are downloaded/built this way are unpacked
    into a site-packages directory, to be included in the bundle by the
    packager.
    """
    _MANYLINUX_COMPATIBLE_PLATFORM = {"any", "linux_x86_64",
                                      "manylinux1_x86_64"}
    _COMPATIBLE_PACKAGE_WHITELIST = {
        "sqlalchemy"
    }

    def __init__(self, osutils=None, ui=None, pip_runner=None, force_download=False):
        self._osutils = osutils or OSUtils()
        self._ui = ui
        if pip_runner is None:
            pip_runner = PipRunner(SubprocessPip(self._osutils))
        self._pip = pip_runner
        self.force_download = force_download

    def _is_compatible_wheel_filename(self, filename):
        wheel = filename[:-4]
        implementation, abi, platform = wheel.split("-")[-3:]
        # Verify platform is compatible
        if platform not in self._MANYLINUX_COMPATIBLE_PLATFORM:
            return False
        # Verify that the ABI is compatible with lambda. Either none or the
        # correct type for the python version cp27mu for py27 and cp36m for
        # py36.
        if abi == "none":
            return True
        prefix_version = implementation[:3]
        if prefix_version == "cp3":
            # Deploying python 3 function which means we need cp36m abi
            # We can also accept abi3 which is the CPython 3 Stable ABI and
            # will work on any version of python 3.
            return abi == "cp36m" or abi == "abi3"
        elif prefix_version == "cp2":
            # Deploying to python 2 function which means we need cp27mu abi
            return abi == "cp27mu"
        # Don"t know what we have but it didn"t pass compatibility tests.
        return False

    def _has_at_least_one_package(self, filename):
        if not self._osutils.file_exists(filename):
            return False
        with open(filename, "r") as f:
            # This is meant to be a best effort attempt.
            # This can return True and still have no packages
            # actually being specified, but those aren"t common
            # cases.
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    return True
        return False

    def _download_all_dependencies(self, requirements_filename, directory):
        # Download dependencies prefering wheel files but falling back to
        # raw source dependences to get the transitive closure over
        # the dependency graph. Return the set of all package objects
        # which will serve as the master list of dependencies needed to deploy
        # successfully.
        self._pip.download_all_dependencies(requirements_filename, directory)
        deps = {Package(directory, filename) for filename
                in self._osutils.get_directory_contents(directory)}
        return deps

    def _download_binary_wheels(self, packages, directory):
        # Try to get binary wheels for each package that isn"t compatible.
        self._pip.download_manylinux_wheels(
            [pkg.identifier for pkg in packages], directory)

    def _build_sdists(self, sdists, directory, compile_c=True):
        for sdist in sdists:
            path_to_sdist = self._osutils.joinpath(directory, sdist.filename)
            self._pip.build_wheel(path_to_sdist, directory, compile_c)

    def _categorize_wheel_files(self, directory):
        final_wheels = [Package(directory, filename) for filename
                        in self._osutils.get_directory_contents(directory)
                        if filename.endswith(".whl")]

        compatible_wheels, incompatible_wheels = set(), set()
        for wheel in final_wheels:
            if self._is_compatible_wheel_filename(wheel.filename):
                compatible_wheels.add(wheel)
            else:
                incompatible_wheels.add(wheel)
        return compatible_wheels, incompatible_wheels

    def _download_dependencies(self, directory, requirements_filename):
        deps = self._download_all_dependencies(
            requirements_filename, directory)

        # Sort the downloaded packages into three categories:
        # - sdists (Pip could not get a wheel so it gave us an sdist)
        # - lambda compatible wheel files
        # - lambda incompatible wheel files
        # Pip will give us a wheel when it can, but some distributions do not
        # ship with wheels at all in which case we will have an sdist for it.
        # In some cases a platform specific wheel file may be availble so pip
        # will have downloaded that, if our platform does not match the
        # platform lambda runs on (linux_x86_64/manylinux) then the downloaded
        # wheel file may not be compatible with lambda. Pure python wheels
        # still will be compatible because they have no platform dependencies.
        compatible_wheels = set()
        incompatible_wheels = set()
        sdists = set()
        for package in deps:
            if package.dist_type == "sdist":
                sdists.add(package)
            else:
                if self._is_compatible_wheel_filename(package.filename):
                    compatible_wheels.add(package)
                else:
                    incompatible_wheels.add(package)

        # Next we need to go through the downloaded packages and pick out any
        # dependencies that do not have a compatible wheel file downloaded.
        # For these packages we need to explicitly try to download a
        # compatible wheel file.
        missing_wheels = sdists | incompatible_wheels
        self._download_binary_wheels(missing_wheels, directory)

        # Re-count the wheel files after the second download pass. Anything
        # that has an sdist but not a valid wheel file is still not going to
        # work on lambda and we must now try and build the sdist into a wheel
        # file ourselves.
        compatible_wheels, incompatible_wheels = self._categorize_wheel_files(
            directory)
        missing_wheels = sdists - compatible_wheels
        self._build_sdists(missing_wheels, directory, compile_c=True)

        # There is still the case where the package had optional C dependencies
        # for speedups. In this case the wheel file will have built above with
        # the C dependencies if it managed to find a C compiler. If we are on
        # an incompatible architecture this means the wheel file generated will
        # not be compatible. If we categorize our files once more and find that
        # there are missing dependencies we can try our last ditch effort of
        # building the package and trying to sever its ability to find a C
        # compiler.
        compatible_wheels, incompatible_wheels = self._categorize_wheel_files(
            directory)
        missing_wheels = sdists - compatible_wheels
        self._build_sdists(missing_wheels, directory, compile_c=False)

        # Final pass to find the compatible wheel files and see if there are
        # any unmet dependencies left over. At this point there is nothing we
        # can do about any missing wheel files. We tried downloading a
        # compatible version directly and building from source.
        compatible_wheels, incompatible_wheels = self._categorize_wheel_files(
            directory)

        # Now there is still the case left over where the setup.py has been
        # made in such a way to be incompatible with python"s setup tools,
        # causing it to lie about its compatibility. To fix this we have a
        # manually curated whitelist of packages that will work, despite
        # claiming otherwise.
        compatible_wheels, incompatible_wheels = self._apply_wheel_whitelist(
            compatible_wheels, incompatible_wheels)
        missing_wheels = deps - compatible_wheels

        return compatible_wheels, missing_wheels

    def _apply_wheel_whitelist(self, compatible_wheels, incompatible_wheels):
        compatible_wheels = set(compatible_wheels)
        actual_incompatible_wheels = set()
        for missing_package in incompatible_wheels:
            if missing_package.name in self._COMPATIBLE_PACKAGE_WHITELIST:
                compatible_wheels.add(missing_package)
            else:
                actual_incompatible_wheels.add(missing_package)
        return compatible_wheels, actual_incompatible_wheels

    def _install_purelib_and_platlib(self, wheel, root):
        # Take a wheel package and the directory it was just unpacked into and
        # unpackage the purelib/platlib directories if they are present into
        # the parent directory. On some systems purelib and platlib need to
        # be installed into separate locations, for lambda this is not the case
        # and both should be installed in site-packages.
        data_dir = self._osutils.joinpath(root, wheel.data_dir)
        if not self._osutils.directory_exists(data_dir):
            return
        unpack_dirs = {"purelib", "platlib"}
        data_contents = self._osutils.get_directory_contents(data_dir)
        for content_name in data_contents:
            if content_name in unpack_dirs:
                source = self._osutils.joinpath(data_dir, content_name)
                self._osutils.copytree(source, root)
                # No reason to keep the purelib/platlib source directory around
                # so we delete it to conserve space in the package.
                self._osutils.rmtree(source)

    def _install_wheels(self, src_dir, dst_dir, wheels):
        if self._osutils.directory_exists(dst_dir):
            self._osutils.rmtree(dst_dir)
        self._osutils.makedirs(dst_dir)
        for wheel in wheels:
            zipfile_path = self._osutils.joinpath(src_dir, wheel.filename)
            self._osutils.extract_zipfile(zipfile_path, dst_dir)
            self._install_purelib_and_platlib(wheel, dst_dir)

    def _build_single_package(self, location, package_name, directory):
        try:
            if package_name in constants.PACKAGE_EXLUDE_LIB:
                return
            package_module = sys.modules[package_name]
            if package_module.__file__.endswith('__init__.py'):
                package_path = self._osutils.joinpath(location, package_name)
                destination = self._osutils.joinpath(directory, package_name)
                self._osutils.copytree(package_path, destination)
                self._ui.write('copy package path: %s\n' % package_path)
            else:
                self._osutils.copy(package_module.__file__, directory)
                self._ui.write('copy package file: %s\n' % package_module.__file__)
        except KeyError:
            pass

    def build_local_packages(self, directory):
        for package_name, dist in get_intersected_distributions().items():
            try:
                package_name = list(dist.get_metadata_lines('top_level.txt'))
            except:
                if package_name not in sys.modules:
                    raise InvalidSourceDistributionNameError(
                        f'{package_name} package not installed.')
            if isinstance(package_name, str):
                package_name = [package_name]
            for p_name in package_name:
                self._build_single_package(dist.location, p_name, directory)

    def build_site_packages(self, requirements_filepath, target_directory):
        if self._has_at_least_one_package(requirements_filepath):
            if self.force_download:
                with self._osutils.tempdir() as tempdir:
                    wheels, packages_without_wheels = self._download_dependencies(
                        tempdir, requirements_filepath)
                    self._install_wheels(tempdir, target_directory, wheels)
                    if packages_without_wheels:
                        raise MissingDependencyError(packages_without_wheels)
            else:
                self.build_local_packages(target_directory)


class Package(object):
    """A class to represent a package downloaded but not yet installed."""
    def __init__(self, directory, filename, osutils=None):
        self.dist_type = "wheel" if filename.endswith(".whl") else "sdist"
        self._directory = directory
        self.filename = filename
        self._osutils = osutils or OSUtils()
        self._name, self._version = self._calculate_name_and_version()

    @property
    def name(self):
        return self._name

    @property
    def data_dir(self):
        # The directory format is {distribution}-{version}.data
        return "%s-%s.data" % (self._name, self._version)

    def _normalize_name(self, name):
        # Taken directly from PEP 503
        return re.sub(r"[-_.]+", "-", name).lower()

    @property
    def identifier(self):
        return "%s==%s" % (self._name, self._version)

    def __str__(self):
        return "%s(%s)" % (self.identifier, self.dist_type)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, Package):
            return False
        return self.identifier == other.identifier

    def __hash__(self):
        return hash(self.identifier)

    def _calculate_name_and_version(self):
        if self.dist_type == "wheel":
            # From the wheel spec (PEP 427)
            # {distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-
            # {platform tag}.whl
            name, version = self.filename.split("-")[:2]
        else:
            info_fetcher = SDistMetadataFetcher(osutils=self._osutils)
            sdist_path = self._osutils.joinpath(self._directory, self.filename)
            name, version = info_fetcher.get_package_name_and_version(
                sdist_path)
        normalized_name = self._normalize_name(name)
        return normalized_name, version


class SDistMetadataFetcher(object):
    """This is the "correct" way to get name and version from an sdist."""
    # https://git.io/vQkwV
    _SETUPTOOLS_SHIM = (
        "import setuptools, tokenize;__file__=%r;"
        "f=getattr(tokenize, 'open', open)(__file__);"
        "code=f.read().replace('\\r\\n', '\\n');"
        "f.close();"
        "exec(compile(code, __file__, 'exec'))"
    )

    def __init__(self, osutils=None):
        if osutils is None:
            osutils = OSUtils()
        self._osutils = osutils

    def _parse_pkg_info_file(self, filepath):
        # The PKG-INFO generated by the egg-info command is in an email feed
        # format, so we use an email feedparser here to extract the metadata
        # from the PKG-INFO file.
        data = self._osutils.get_file_contents(filepath, binary=False)
        parser = FeedParser()
        parser.feed(data)
        return parser.close()

    def _generate_egg_info(self, package_dir):
        setup_py = self._osutils.joinpath(package_dir, "setup.py")
        script = self._SETUPTOOLS_SHIM % setup_py

        cmd = [sys.executable, "-c", script, "--no-user-cfg", "egg_info",
               "--egg-base", "egg-info"]
        egg_info_dir = self._osutils.joinpath(package_dir, "egg-info")
        self._osutils.makedirs(egg_info_dir)
        p = subprocess.Popen(cmd, cwd=package_dir,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()
        info_contents = self._osutils.get_directory_contents(egg_info_dir)
        pkg_info_path = self._osutils.joinpath(
            egg_info_dir, info_contents[0], "PKG-INFO")
        return pkg_info_path

    def _unpack_sdist_into_dir(self, sdist_path, unpack_dir):
        if sdist_path.endswith(".zip"):
            self._osutils.extract_zipfile(sdist_path, unpack_dir)
        elif sdist_path.endswith((".tar.gz", ".tar.bz2")):
            self._osutils.extract_tarfile(sdist_path, unpack_dir)
        else:
            raise InvalidSourceDistributionNameError(sdist_path)
        # There should only be one directory unpacked.
        contents = self._osutils.get_directory_contents(unpack_dir)
        return self._osutils.joinpath(unpack_dir, contents[0])

    def get_package_name_and_version(self, sdist_path):
        with self._osutils.tempdir() as tempdir:
            package_dir = self._unpack_sdist_into_dir(sdist_path, tempdir)
            pkg_info_filepath = self._generate_egg_info(package_dir)
            metadata = self._parse_pkg_info_file(pkg_info_filepath)
            name = metadata["Name"]
            version = metadata["Version"]
        return name, version


class SubprocessRunner(object):
    def __init__(self, os_utils=None, import_string=None):
        if os_utils is None:
            os_utils = OSUtils()
        self._os_utils = os_utils
        if import_string is None:
            import_string = pip_import_string()
        self._import_string = import_string

    def get_exec_string(self, args):
        return ""

    def main(self, args=None, env_vars=None, shim=None):
        if env_vars is None:
            env_vars = self._os_utils.environ()
        if shim is None:
            shim = ''
        python_exe = sys.executable
        exec_string = "%s%s" % (shim, self.get_exec_string(args))
        invoke_command = [python_exe, "-c", exec_string]
        p = self._os_utils.popen(invoke_command,
                                 stdout=self._os_utils.pipe,
                                 stderr=self._os_utils.pipe,
                                 env=env_vars)
        out, err = p.communicate()
        rc = p.returncode
        return rc, out, err


class SubprocessPip(SubprocessRunner):

    def get_exec_string(self, args):
        return (
            "import sys; %s; sys.exit(main(%s))"
        ) % (self._import_string, args)


class SubprocessRequire(SubprocessRunner):

    def get_exec_string(self, args):
        return (
            "%s;import app;import importreqs; open('requirements.txt','w').write(\
            importreqs.generate_reqs(exclude=%s)); sys.exit(main(%s))"
        ) % (self._import_string, constants.PACKAGE_EXLUDE_LIB, args)


class PipRunner(object):
    _LINK_IS_DIR_PATTERN = ("Processing (.+?)\n"
                            "  Link is a directory,"
                            " ignoring download_dir")

    def __init__(self, pip, osutils=None):
        if osutils is None:
            osutils = OSUtils()
        self._wrapped_pip = pip
        self._osutils = osutils

    def _execute(self, command, args, env_vars=None, shim=None):
        """Execute a pip command with the given arguments."""
        main_args = [command] + args
        rc, out, err = self._wrapped_pip.main(main_args, env_vars=env_vars,
                                              shim=shim)
        return rc, out, err

    def build_wheel(self, wheel, directory, compile_c=True):
        """Build an sdist into a wheel file."""
        arguments = ["--no-deps", "--wheel-dir", directory, wheel]
        env_vars = self._osutils.environ()
        shim = ''
        if not compile_c:
            env_vars.update(pip_no_compile_c_env_vars)
            shim = pip_no_compile_c_shim
        # Ignore rc and stderr from this command since building the wheels
        # may fail and we will find out when we categorize the files that were
        # generated.
        self._execute("wheel", arguments,
                      env_vars=env_vars, shim=shim)

    def download_all_dependencies(self, requirements_filename, directory):
        """Download all dependencies as sdist or wheel."""
        arguments = ["-r", requirements_filename, "--dest", directory]
        rc, out, err = self._execute("download", arguments)
        if rc != 0:
            if err is None:
                err = b"Unknown error"
            error = err.decode()
            match = re.search(("Could not find a version that satisfies the "
                               "requirement (.+?) "), error)
            if match:
                package_name = match.group(1)
                raise NoSuchPackageError(str(package_name))
            raise PackageDownloadError(error)
        stdout = out.decode()
        match = re.search(self._LINK_IS_DIR_PATTERN, stdout)
        if match:
            wheel_package_path = str(match.group(1))
            self.build_wheel(wheel_package_path, directory)

    def download_manylinux_wheels(self, packages, directory):
        for package in packages:
            arguments = ["--only-binary=:all:", "--no-deps", "--platform",
                         "manylinux1_x86_64", "--implementation", "cp",
                         "--abi", lambda_abi, "--dest", directory, package]
            self._execute("download", arguments)


class SAMTemplateGenerator(object):
    _BASE_TEMPLATE = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Transform": "AWS::Serverless-2016-10-31",
        "Outputs": {},
        "Resources": {},
    }

    def generate_lambda_function(self, model):
        template = self._BASE_TEMPLATE
        lambda_function_definition = {
            "Type": "AWS::Serverless::Function",
            "Properties": {
                "Runtime": model.runtime,
                "Handler": model.handler,
                "CodeUri": model.filename,
                "Tags": model.tags,
                "Timeout": model.timeout,
                "MemorySize": model.memory_size,
                "FunctionName": model.function_name
            }
        }
        if model.environment:
            environment_config = {
                "Environment": {
                    "Variables": model.environment
                }
            }
            lambda_function_definition["Properties"].update(environment_config)
        if model.security_group_ids and model.subnet_ids:
            vpc_config = {
                "VpcConfig": {
                    "SecurityGroupIds": model.security_group_ids,
                    "SubnetIds": model.subnet_ids,
                }
            }
            lambda_function_definition["Properties"].update(vpc_config)
        if model.role:
            lambda_function_definition["Properties"].update(Role=model.role)
        template["Resources"]["Index"] = lambda_function_definition
        return template


class AppBuilder(object):
    def __init__(self, app, os_utils, ui, stage):
        self._app = app
        self._os_utils = os_utils
        self._ui = ui
        self._stage = stage

    def _to_json(self, doc):
        return serialize_to_json(doc)

    @property
    def tags(self):
        return dict(aws_app="version=%s:stage=%s:app=%s" % (
            constants.APP_VERSION, self._stage, self._app.app_name))

    @property
    def stage_name(self):
        return "%s-%s" % (self._app.app_name, self._stage)

    @property
    def index_function_name(self):
        return "%s-%s-%s" % (self._app.app_name, self._stage,
                             self._app.index_lambda_function.name)

    @property
    def s3_bucket(self):
        return self._app.config["AWS_S3_BUCKET"]

    def gen_s3_key_from_deploy_file(self, deploy_file):
        return "%s/dist_%s_%s.zip" % (
            self.stage_name, datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
            OSUtils().md5_file(deploy_file)
        )

    def create_lambda_function(self, package_filename=None):
        return models.LambdaFunction(
            self._app.root_path, self._stage,
            self.index_function_name,
            self._app.index_lambda_function.handler,
            self.tags, package_filename,
            self._app.config["LAMBDA_RUN_TIME"],
            self._app.config["LAMBDA_TIMEOUT"],
            self._app.config["LAMBDA_MEMORY_SIZE"],
            self._app.config["LAMBDA_ROLE"],
            self._app.config["LAMBDA_SECURITY_GROUP_IDS"],
            self._app.config["LAMBDA_SUBNET_IDS"],
            self._app.lambda_environment
        )


class AppPackager(AppBuilder):
    def __init__(self, app, os_utils, ui, stage, sam_templater, deploy_packager):
        super(AppPackager, self).__init__(app, os_utils, ui, stage)
        self._sam_templater = sam_templater
        self._deploy_packager = deploy_packager

    def package_app(self, out_dir, generate_sam=False):
        # Deployment package
        package_filename = self._os_utils.joinpath(
            self._app.root_path, out_dir, constants.DEFAULT_PACKAGE_FILE)
        self._deploy_packager.create_deployment_package(package_filename)
        # SAM template
        if generate_sam:
            sam_template = self._sam_templater.generate_lambda_function(
                self.create_lambda_function(package_filename))
            if not self._os_utils.directory_exists(out_dir):
                self._os_utils.makedirs(out_dir)
            self._os_utils.set_file_contents(
                filename=os.path.join(out_dir, constants.DEFAULT_SAM_FILE),
                contents=self._to_json(sam_template),
                binary=False
            )
        return package_filename


if __name__ == '__main__':
    from aws_lambda_sls.utils import OSUtils, UI
    ui, os_utils = UI(), OSUtils()
    pip_runner = PipRunner(
        pip=SubprocessPip(os_utils=os_utils),
        osutils=os_utils
    )
    dependency_builder = PipDependencyBuilder(
        osutils=os_utils, ui=ui,
        pip_runner=pip_runner,
        force_download=True
    )
    dependency_builder.build_local_packages('dist')
