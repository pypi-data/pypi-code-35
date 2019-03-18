# -*- coding: utf-8 -*-

"""
Include YAML files within YAML
"""

import io
import os.path
import re
from glob import iglob
from sys import version_info

import yaml

__all__ = ['YamlIncludeConstructor']

PYTHON_MAYOR_MINOR = '{0[0]}.{0[1]}'.format(version_info)

WILDCARDS_REGEX = re.compile(r'^.*(\*|\?|\[!?.+\]).*$')


class YamlIncludeConstructor:
    """The `include constructor` for PyYAML's loader

    Call :meth:`add_to_loader_class` or :meth:`yaml.Loader.add_constructor` to add it into loader.

    In YAML files, use ``!include`` to load other YAML files as below::

        !include [dir/**/*.yml, true]

    or::

        !include {pathname: dir/abc.yml, encoding: utf-16}

    """

    DEFAULT_ENCODING = 'utf-8'
    DEFAULT_TAG_NAME = '!include'

    def __init__(self, base_dir=None, encoding=None):
        # type:(str, str)->YamlIncludeConstructor
        """
        :param str base_dir: Base directory from where finding YAML files
        :param str encoding: encoding of the YAML files

            * `None`: load YAML files from current working directory.
        """
        self._base_dir = base_dir
        self._encoding = encoding

    def __call__(self, loader, node):
        args = []
        kwargs = {}
        if isinstance(node, yaml.nodes.ScalarNode):
            args = [loader.construct_scalar(node)]
        elif isinstance(node, yaml.nodes.SequenceNode):
            args = loader.construct_sequence(node)
        elif isinstance(node, yaml.nodes.MappingNode):
            kwargs = loader.construct_mapping(node)
        else:
            raise TypeError('Un-supported YAML node {!r}'.format(node))
        return self.load(loader, *args, **kwargs)

    @property
    def base_dir(self):  # type: ()->str
        # pylint:disable=missing-docstring
        return self._base_dir

    @base_dir.setter
    def base_dir(self, value):  # type: (str)->None
        self._base_dir = value

    @property
    def encoding(self):  # type: ()->str
        # pylint:disable=missing-docstring
        return self._encoding

    @encoding.setter
    def encoding(self, value):  # type: (str)->None
        self._encoding = value

    def load(self, loader, pathname, recursive=False, encoding=None):
        """Once add the constructor to PyYAML loader class,
        Loader will use this function to include other YAML fils
        on parsing ``"!include"`` tag

        :param loader: Instance of PyYAML's loader class
        :param str pathname: pathname can be either absolute (like /usr/src/Python-1.5/Makefile) or relative (like ../../Tools/*/*.gif), and can contain shell-style wildcards

        :param bool recursive: If recursive is true, the pattern ``"**"`` will match any files and zero or more directories and subdirectories. If the pattern is followed by an os.sep, only directories and subdirectories match.

            Note:
             Using the ``"**"`` pattern in large directory trees may consume an inordinate amount of time.

        :param str encoding: YAML file encoding

            :default: ``None``: :attr:`encoding` or :attr:`DEFAULT_ENCODING` will be used

        :return: included YAML file, in Python data type

        .. warning:: It's called by :mod:`yaml`. Do NOT call it yourself.
        """
        if not encoding:
            encoding = self._encoding or self.DEFAULT_ENCODING
        if self._base_dir:
            pathname = os.path.join(self._base_dir, pathname)
        if WILDCARDS_REGEX.match(pathname):
            result = []
            if PYTHON_MAYOR_MINOR >= '3.5':
                iterator = iglob(pathname, recursive=recursive)
            else:
                iterator = iglob(pathname)
            for path in iterator:
                if os.path.isfile(path):
                    with io.open(path, encoding=encoding) as f:  # pylint:disable=invalid-name
                        result.append(yaml.load(f, type(loader)))
            return result
        with io.open(pathname, encoding=encoding) as f:  # pylint:disable=invalid-name
            return yaml.load(f, type(loader))

    @classmethod
    def add_to_loader_class(cls, loader_class, tag=None, **kwargs):
        # type: (type(yaml.Loader), str, **str)-> yamlincludeconstructor
        """
        Create an instance of the constructor, and add it to the YAML `Loader` class

        :param loader_class:
          The `Loader` class add constructor to.

          :default: ``None``: Add to PyYAML's default `Loader`

        :type loader_class: type(yaml.SafeLoader) | type(yaml.Loader) | type(yaml.CSafeLoader) | type(yaml.FullLoader)

        :param str tag:
          tag name for the include constructor.

          :default: ``""``: use :attr:`DEFAULT_TAG_NAME` as tag name.

        :param kwargs: Arguments passed to constructor

        :return: New created object
        :rtype: YamlIncludeConstructor
        """
        if tag is None:
            tag = ''
        tag = tag.strip()
        if not tag:
            tag = cls.DEFAULT_TAG_NAME
        if not tag.startswith('!'):
            raise ValueError('`tag` argument should start with character "!"')
        instance = cls(**kwargs)
        yaml.add_constructor(tag, instance, loader_class)
        return instance
