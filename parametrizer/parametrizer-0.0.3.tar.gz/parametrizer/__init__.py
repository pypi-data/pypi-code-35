# -*- coding: utf-8 -*-

import json
from string import Template

from jinja2 import Template as Jinja2Template


class Parametrizer(object):
    """ This class let you parametrize your strings
        and convert them to regular Python dictionaries.

        It supports also json.

        Let's try with a **matching name**

        >>> value = '{"baudrate": $baudrate_value}'
        >>> mapping = {"baudrate_value": 250, "name": "a name"}
        >>> parametrizer = Parametrizer(mapping)

        With the ``parametrize`` method you'll get a parametrized
        string:

        >>> parametrizer.parametrize(value)
        '{"baudrate": 250}'


        With the ``json_loads`` method you'll get a parametrized regular
        Python mapping:

        >>> parametrizer.json_loads(value) == {'baudrate': 250}
        True

        And now with **non matching names**

        >>> value = '{"name": "$a_name"}'
        >>> mapping = {"name": "a name"}
        >>> parametrizer = Parametrizer(mapping)

        With the ``parametrize`` method you'll get a parametrized
        string:

        >>> parametrizer.parametrize(value)
        '{"name": "$a_name"}'


        With the ``json_loads`` method you'll get a parametrized regular
        Python mapping:

        >>> parametrizer.json_loads(value) == {'name': '$a_name'}
        True

        And **json not valid**

        >>> value = '{"name": $name}'
        >>> mapping = {"name": "a name"}
        >>> parametrizer = Parametrizer(mapping)

        With the ``parametrize`` method you'll get a parametrized
        string:

        >>> parametrizer.parametrize(value)
        '{"name": a name}'


        Depending on Python version 2 vs 3 you will get a different exception:

        * json.decoder.JSONDecodeError: Expecting value: ...
        * ValueError: No JSON object could be decoded

        >>> import pytest
        >>> with pytest.raises(Exception):
        ...     parametrizer.json_loads(value)


        >>> value = '{"name": "{! name.upper() !}"}'
        >>> mapping = {"name": "a name"}
        >>> parametrizer = Parametrizer(mapping)

        With the ``parametrize`` method you'll get a parametrized
        string:

        >>> parametrizer.parametrize(value)
        '{"name": "A NAME"}'

        >>> import string
        >>> context = {
        ...     'variables': {'foo': 'bar', 'barbaz': 'bar baz'},
        ...     'capwords': string.capwords}
        >>> parametrizer = Parametrizer(context['variables'],
        ...     context=context)
        >>> parametrizer.parametrize('$foo')
        'bar'
        >>> parametrizer.parametrize('{! variables["foo"].upper() !}')
        'BAR'
        >>> parametrizer.parametrize('{! "$foo".upper() !}')
        'BAR'
        >>> parametrizer.parametrize('{! capwords(variables["barbaz"]) !}')
        'Bar Baz'
        >>> parametrizer.parametrize('{! capwords("$barbaz") !}')
        'Bar Baz'
    """

    def __init__(self, mapping, context={}):
        self.mapping = mapping
        self.context = context or mapping

    def parametrize(self, value):
        """ Return the value with template substitution """
        template = Template(value)
        return Jinja2Template(
            template.safe_substitute(**self.mapping),
            variable_start_string='{!',
            variable_end_string='!}').render(
                **self.context)

    def json_loads(self, value):
        """ Return the json load of template substitution """
        parametrized = self.parametrize(value)
        return json.loads(parametrized)
