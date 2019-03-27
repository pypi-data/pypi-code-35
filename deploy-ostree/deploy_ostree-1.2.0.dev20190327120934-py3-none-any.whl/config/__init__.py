# Copyright 2018, 2019 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import json
import os.path
from pathlib import Path
from typing import Iterable, Optional, TextIO, Mapping
from uuid import uuid4
from .error import InvalidConfigError
from .provisioners import ProvisionerConfig, get_provisioners
from .provisioners import BuiltinProvisionerConfig, ScriptProvisionerConfig  # noqa
from .rootfs import get_root_fs


def random_string() -> str:
    return uuid4().hex[:12]


class Source:
    def __init__(self, type: str, value: str) -> None:
        self.type = type
        self.value = value

    @staticmethod
    def url(value: str):
        return Source('url', value)

    @staticmethod
    def path(value: str):
        return Source('path', value)

    @property
    def is_url(self):
        return self.type == 'url'

    @property
    def is_path(self):
        return self.type == 'path'


class Config:
    def __init__(
        self,
        source: Source,
        ref: str,
        *,
        base_dir: str = '',
        sysroot: Optional[str] = None,
        root_filesystem: Optional[str] = None,
        fstab: Path = None,
        remote: Optional[str] = None,
        stateroot: Optional[str] = None,
        kernel_args: Iterable[str] = (),
        provisioners: Iterable[ProvisionerConfig] = ()
    ) -> None:
        self._source = source
        self.ref = ref
        self.base_dir = base_dir
        self.sysroot = sysroot or '/'
        self.root_filesystem = root_filesystem or get_root_fs()
        self.fstab = fstab or Path('/', 'etc', 'fstab')
        self.remote = remote or random_string()
        self.stateroot = stateroot or random_string()
        self.kernel_args = list(kernel_args)
        self.provisioners = list(provisioners)
        self.deployment_name = None  # type: Optional[str]

    @property
    def url(self) -> Optional[str]:
        return self._source.value if self._source.is_url else None

    @property
    def path(self) -> Optional[str]:
        return os.path.join(self.base_dir, self._source.value) if self._source.is_path else None

    @property
    def var_dir(self) -> str:
        return os.path.join(self.sysroot, 'ostree', 'deploy', self.stateroot, 'var')

    @property
    def deployment_dir(self) -> str:
        if self.deployment_name is None:
            raise RuntimeError('deployment name not set')
        return os.path.join(
            self.sysroot,
            'ostree', 'deploy', self.stateroot,
            'deploy', self.deployment_name
        )

    @property
    def ostree_repo(self) -> str:
        return os.path.join(self.sysroot, 'ostree', 'repo')

    def set_deployment_name(self, deployment: str) -> None:
        self.deployment_name = deployment

    @classmethod
    def parse_json(
        cls,
        fobj: TextIO, *,
        base_dir: str = '',
        sysroot: Optional[str] = None,
        root_filesystem: Optional[str] = None,
        fstab: Path = None
    ) -> 'Config':
        try:
            data = json.load(fobj)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise InvalidConfigError(str(exc))

        if not isinstance(data, Mapping):
            raise InvalidConfigError('top-level value must be object')

        if 'url' in data and 'path' in data:
            raise InvalidConfigError("both 'url' and 'path' are present")
        elif 'url' in data:
            source = Source.url(data['url'])
        elif 'path' in data:
            source = Source.path(data['path'])
        else:
            raise InvalidConfigError("neither 'url' nor 'path' are present")

        try:
            return cls(
                source=source,
                ref=data['ref'],
                base_dir=base_dir,
                sysroot=sysroot,
                root_filesystem=root_filesystem,
                fstab=fstab,
                remote=data.get('remote'),
                stateroot=data.get('stateroot'),
                kernel_args=data.get('kernel-args', ()),
                provisioners=get_provisioners(data),
            )
        except KeyError as exc:
            raise InvalidConfigError("missing key '{}'".format(exc.args[0]))
