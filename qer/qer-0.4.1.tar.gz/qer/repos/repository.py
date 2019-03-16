from __future__ import print_function

import abc
import struct
import enum
import platform
import re
import sys

import pkg_resources
import six

import qer.metadata
import qer.utils

INTERPRETER_TAGS = {
    'CPython': 'cp',
    'IronPython': 'ip',
    'PyPy': 'pp',
    'Jython': 'jy',
}


def _get_platform_tag():
    is_32 = struct.calcsize("P") == 4
    if sys.platform == 'win32':
        if is_32:
            tag = 'win32'
        else:
            tag = 'win_amd64'
    elif sys.platform.startswith('linux'):
        if is_32:
            tag = 'manylinux1_' + platform.machine()
        else:
            tag = 'manylinux1_x86_64'
    else:
        raise ValueError('Unsupported platform: {}'.format(sys.platform))
    return tag


INTERPRETER_TAG = INTERPRETER_TAGS.get(platform.python_implementation(), 'cp')
PY_VERSION_NUM = str(sys.version_info.major) + str(sys.version_info.minor)
IMPLEMENTATION_TAGS = ('py2' if six.PY2 else 'py3',
                       INTERPRETER_TAG + PY_VERSION_NUM,
                       'py' + PY_VERSION_NUM)

PLATFORM_TAG = _get_platform_tag()
EXTENSIONS = ('.whl', '.tar.gz', '.tgz', '.zip')


class DistributionType(enum.Enum):
    WHEEL = 1
    SDIST = 0


class RequiresPython(object):
    def __init__(self, py_version):
        self.py_version = py_version

    def check_compatibility(self):
        if self.py_version is None:
            return True
        if isinstance(self.py_version, tuple):
            return self.py_version == () or any(version in IMPLEMENTATION_TAGS for version in self.py_version)

        parts = self.py_version.split(',')
        system_py_version = pkg_resources.parse_version(sys.version.split(' ')[0])

        ops = {
            '<': lambda x, y: x < y,
            '>': lambda x, y: x > y,
            '==': lambda x, y: x == y,
            '!=': lambda x, y: x != y,
            '>=': lambda x, y: x >= y,
            '<=': lambda x, y: x <= y
        }

        results = []
        for part in parts:
            ref_version = system_py_version
            part = part.strip()
            version_part = re.split('[!=<>~]', part)[-1].strip()
            operator = part.replace(version_part, '').strip()
            if version_part.endswith('.*'):
                version_part = version_part.replace('.*', '')
                dotted_parts = len(version_part.split('.'))
                if dotted_parts == 2:
                    ref_version = pkg_resources.parse_version('{}.{}'.format(sys.version_info.major,
                                                                             sys.version_info.minor))
                if dotted_parts == 1:
                    ref_version = pkg_resources.parse_version('{}'.format(sys.version_info.major))

            version = pkg_resources.parse_version(version_part)
            results.append(ops[operator](ref_version, version))

        return all(results)

    @property
    def tag_score(self):
        result = 100
        version_val = None
        if not isinstance(self.py_version, tuple):
            version_val = self.py_version
        elif len(self.py_version) == 1:
            version_val = self.py_version[0]

        if version_val is not None:
            for tag_type in tuple(INTERPRETER_TAGS.values()) + ('py',):
                version_val = version_val.replace(tag_type, '')
            try:
                result += int(version_val)
            except ValueError:
                pass

        return result

    def __eq__(self, other):
        return self.py_version == other.py_version

    def __str__(self):
        if self.py_version is None:
            return 'any'

        if isinstance(self.py_version, tuple):
            return ','.join(self.py_version)
        return ''


class Candidate(object):
    def __init__(self, name, filename, version, py_version, platform, link,
                 candidate_type=DistributionType.SDIST):
        """

        Args:
            name:
            filename:
            version:
            py_version (RequiresPython): Python version
            platform:
            link:
            type:
        """
        self.name = name
        self.filename = filename
        self.version = version
        self.py_version = py_version   # type: RequiresPython
        self.platform = platform
        self.link = link
        self.type = candidate_type

        # Sort based on tags to make sure the most specific distributions
        # are matched first
        # self.sortkey = (candidate_type.value, version, self.tag_score)
        # self.sortkey = (version, self.tag_score)
        self.sortkey = (version, candidate_type.value, self.tag_score)

    def _calculate_tag_score(self):
        tag_score = self.py_version.tag_score
        if platform != 'any':
            tag_score += 1000

        return tag_score

    @property
    def tag_score(self):
        result = self.py_version.tag_score
        if platform != 'any':
            result += 1000

        return result

    def __eq__(self, other):
        return (self.name == other.name and
                self.filename == other.filename and
                self.version == other.version and
                self.py_version == other.py_version and
                self.platform == other.platform and
                self.link == other.link and
                self.type == other.type)

    def __repr__(self):
        return 'Candidate(name={}, filename={}, version={}, py_version={}, platform={}, link={})'.format(
            self.name, self.filename, self.version, self.py_version, self.platform, self.link
        )

    def __str__(self):
        py_version_str = str(self.py_version) + '-'
        return '{} {}-{}-{}{}'.format(
            self.type.name,
            self.name, self.version, py_version_str, self.platform)


class NoCandidateException(Exception):
    def __init__(self, *args):
        super(NoCandidateException, self).__init__(*args)
        self.req = None
        self.results = None
        self.constraint_results = None
        self.mapping = None
        self.check_level = 0

    def __str__(self):
        return 'NoCandidateException - no candidate for "{}" satisfies {}'.format(
            self.req.name,
            self.req.specifier
        )


def process_distribution(source, filename, py_version=None):
    candidate = None
    if '.whl' in filename:
        candidate = _wheel_candidate(source, filename)
    elif '.tar.gz' in filename or '.tgz' in filename or '.zip' in filename:
        candidate = _tar_gz_candidate(source, filename, py_version=py_version)
    return candidate


def _wheel_candidate(source, filename):
    data_parts = filename.split('-')
    name = data_parts[0]
    version = pkg_resources.parse_version(data_parts[1])
    plat = data_parts[4].split('.')[0]
    return Candidate(name,
                     filename,
                     version,
                     RequiresPython(tuple(data_parts[2].split('.'))),
                     plat,
                     source,
                     candidate_type=DistributionType.WHEEL)


def _tar_gz_candidate(source, filename, py_version=None):
    name, version = qer.metadata.parse_source_filename(filename)
    return Candidate(name, filename, version, RequiresPython(py_version), 'any',
                     source, candidate_type=DistributionType.SDIST)


def _check_platform_compatibility(py_platform):
    return py_platform == 'any' or py_platform.lower() == PLATFORM_TAG


class BaseRepository(six.with_metaclass(abc.ABCMeta, object)):
    @abc.abstractmethod
    def get_candidate(self, req):
        raise NotImplementedError()

    def source_of(self, req):
        return self


class CantUseReason(enum.Enum):
    U_CAN_USE = 0
    WRONG_PYTHON_VERSION = 2
    WRONG_PLATFORM = 3
    IS_PRERELEASE = 4
    VERSION_NO_SATISFY = 5


class Repository(six.with_metaclass(abc.ABCMeta, BaseRepository)):
    def __init__(self, allow_prerelease=None):
        if allow_prerelease is None:
            allow_prerelease = False

        self.allow_prerelease = allow_prerelease

    @abc.abstractmethod
    def get_candidates(self, req):
        """
        Fetch all available candidates for a project_name
        Args:
            project_name (str): Project name as it appears in a requirements file

        Returns:
            (list) List of candidates
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def resolve_candidate(self, candidate):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def logger(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def close(self):
        raise NotImplementedError()

    def get_candidate(self, req):
        candidates = self.get_candidates(req)
        return self._do_get_candidate(req, candidates)

    def _do_get_candidate(self, req, candidates):
        self.logger.info('Getting candidate for %s', req)
        candidates = self._sort_candidates(candidates)
        has_equality = qer.utils.is_pinned_requirement(req)

        check_level = 1
        for candidate in candidates:
            check_level += 1
            if not candidate.py_version.check_compatibility():
                continue

            check_level += 1
            if not _check_platform_compatibility(candidate.platform):
                continue

            check_level += 1
            if not has_equality and not self.allow_prerelease and candidate.version.is_prerelease:
                continue

            check_level += 1
            if not req.specifier.contains(candidate.version, prereleases=has_equality):
                continue

            check_level += 1
            if candidate.type == DistributionType.SDIST:
                self.logger.warning('Considering source distribution for %s', candidate.name)
            return self.resolve_candidate(candidate)

        ex = NoCandidateException()
        ex.req = req
        ex.check_level = check_level
        raise ex

    def why_cant_I_use(self, req, candidate):
        try:
            self._do_get_candidate(req, (candidate,))
            raise ValueError('This requirement can be used')
        except NoCandidateException as ex:
            return CantUseReason(ex.check_level)

    def _sort_candidates(self, candidates):
        """

        Args:
            candidates:

        Returns:
            (list[Candidate])
        """
        return sorted(candidates, key=lambda x: x.sortkey, reverse=True)
