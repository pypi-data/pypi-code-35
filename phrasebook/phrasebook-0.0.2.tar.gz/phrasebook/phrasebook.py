#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 3/19/19 by Pat Blair
"""
.. currentmodule:: phrasebook.phrasebook
.. moduleauthor:: Pat Blair <pblair@geo-comm.com>

Store phrases (SQL, messages, what-have-you) alongside your modules.
"""
from collections import Mapping
import inspect
from pathlib import Path
from string import Template
from typing import Dict, Iterable, ItemsView, Tuple
import toml


PHRASES_SUFFIX = '.phr'  #: the standard suffix for phrasebook directories


class Phrasebook:
    """
    A phrasebook is an indexed collection of string templates.
    """
    def __init__(
            self,
            path: str or Path = None,
            suffixes: Iterable[str] = None
    ):
        """

        :param path: the path to the phrases directory, or a file that has an
            accompanying phrasebook directory
        :param suffixes: the suffixes of phrase files

        .. seealso::

            `Python's String Templates <https://bit.ly/2FdnQ61>`_
        """
        # Let's figure out where the phrases are kept. (Part One)
        self._path: Path = self._resolve_path(path)

        # We should also keep track of the file suffixes we expect to find.
        self._suffixes: Tuple[str] = tuple(
            (s if s.startswith('.') else f".{s}").lower()
            for s in (
                suffixes if suffixes else []
            ) if s
        ) if suffixes else ()

        # Let's figure out where the phrases are kept. (Part Two)
        if not self._path.exists():  # Say the prescribed path does not exist.
            # Let's look for siblings...
            _parent: Path = self._path.parent
            # ...that may have the same name (stem)...
            for _item in [
                    i for i in _parent.iterdir()
                    if i.stem == self._path.stem
            ]:
                # ...but one of the prescribed suffixes (case-insensitive)...
                if _item.suffix.lower() in self._suffixes:
                    # ...and if we find such a thing, that's the new path.
                    self._path = _item
                    break

        self._phrases: Dict[str, Template] = {}  #: the phrase templates

    @classmethod
    def _resolve_path(cls, path: str or Path):
        return (
            (
                path if isinstance(dir, Path) else Path(path)
            ).expanduser().resolve()
        ) if path else Path(
            getattr(
                inspect.getmodule(inspect.currentframe().f_back.f_back),
                '__file__'
            )
        ).with_suffix(PHRASES_SUFFIX)

    @property
    def path(self) -> Path:
        """
        Get the path to the phrases directory.
        """
        return self._path

    @property
    def suffixes(self) -> Tuple[str]:
        """
        Get the recognized suffixes for phrase files.
        """
        return self._suffixes

    def items(self) -> ItemsView[str, Template]:
        """
        Get the key-value pairs.
        """
        return self._phrases.items()

    def _load_dir(self, path: Path, prefix: str = ''):
        """
        Recursively load a phrases directory.

        :param path: the directory path to load
        :param prefix: the prefix to prepend to all the phrase keys in the
            phrase dictionary
        """
        # Go through all the items in the path.
        for sub in path.iterdir():
            # If this item is a directory, append its name to the current
            # prefix and load it recursively.
            if sub.is_dir():
                self._load_dir(sub, prefix=f"{prefix}{sub.name}.")
            elif (
                    sub.is_file()
                    and (
                        not self._suffixes
                        or sub.suffix.lower() in self.suffixes
                    )
            ):
                # Otherwise, if it's a file and we either have no preference
                # for suffixes, or it's suffix is one we recognize, create a
                # template for it and place it into the dictionary of phrases.
                self._phrases[f"{prefix}{sub.stem}"] = Template(sub.read_text())

    def _load_dict(self, dict_: Mapping, prefix: str = ''):
        """
        Recursively load a dictionary of phrases.

        :param dict_: the phrases dictionary
        :param prefix: the prefix to prepend to all the phrase keys in the
            phrase dictionary
        """
        # Let's look at each of the items...
        for k, v in dict_.items():
            # If the value appears to be a dictionary...
            if isinstance(v, Mapping):
                # ...load it.
                self._load_dict(v, prefix=f"{prefix}{k}.")
            else:
                # Otherwise, we assume it's either a template, or string-like.
                self._phrases[f"{prefix}{k}"] = (
                    v if isinstance(v, Template)
                    else Template(str(v))
                )

    def _load_file(self, path: Path):
        """
        Load a dictionary of phrases from a file.

        :param path: the path to the file
        """
        self._load_dict(toml.loads(path.read_text()))

    def load(self) -> 'Phrasebook':
        """
        Load the phrases.

        :return: this instance
        """
        # Figure out which loader method is appropriate for the path.
        _load_fn = self._load_file if self._path.is_file() else self._load_dir
        # Load 'em up!
        _load_fn(self._path)
        # Always return the current instance.
        return self

    def substitute(
            self,
            phrase: str,
            default: str or Template = None,
            safe: bool = True,
            **kwargs
    ) -> str or None:
        """
        Perform substitutions on a phrase template and return the result.

        :param phrase: the phrase
        :param default: a default template
        :param safe: `True` (the default) to leave the original placeholder in
            the template in place if no matching keyword is found
        :param kwargs: the substitution arguments
        :return: the substitution result
        """
        template = self.get(
            phrase=phrase,
            default=default
        )
        if not template:
            return None
        return (
            template.safe_substitute(**kwargs) if safe
            else template.substitute(**kwargs)
        )

    def get(
            self,
            phrase: str,
            default: str or Template = None
    ) -> Template or None:
        """
        Get a phrase template.

        :param phrase: the name of the phrase template
        :param default: a default template or string
        :return: the template (or the default), or `None` if no template
            is defined

        .. seealso::

            :py:func:`gets`
        """
        try:
            return self._phrases[phrase]
        except KeyError:
            # If we were supplied with a default...
            if default is not None:
                # ...return that.
                return (
                    default if isinstance(default, Template)
                    else Template(default)
                )
            # Otherwise, the caller gets `None`
            return None

    def gets(
            self,
            phrase: str,
            default: str or Template = None
    ) -> str or None:
        """
        Get a phrase template string.

        :param phrase: the name of the phrase template
        :param default: a default template or string
        :return: the template (or the default), or `None` if no template
            is defined
        """
        try:
            # See if the `get` method can give us a `Template` from which we
            # may derive a string.
            return self.get(phrase=phrase, default=default).template
        except (KeyError, AttributeError):
            # If we got a `KeyError` (because the phrase wan't found) or an
            # `AttributeError` (likely because the phrase is found but it's
            # value is `None`), we may be able to revert to the default.
            if default is not None:
                return (
                    default.template if isinstance(default, Template)
                    else default
                )
            # Otherwise, return None.
            return None

    def __contains__(self, item):
        return item in self._phrases
