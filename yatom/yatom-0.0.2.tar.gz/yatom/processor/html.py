from . import base
from . import xml


class HTMLProcessError(base.ProcessError):
    pass


class HTMLProcessor(xml.XMLProcessor):
    exc_class = HTMLProcessError
    autoclose = (
        'area',
        'base',
        'br',
        'col',
        'command',
        'embed',
        'hr',
        'img',
        'input',
        'keygen',
        'link',
        'meta',
        'param',
        'source',
        'track',
        'wbr',
        'text',
        )
    autoclose_all = False
    autoclose_end = '>'
    html4_overrides = {
        'default_attributes': {
            'style': {
                '.type': 'text/css',
                },
            'script': {
                '.type': 'application/javascript',
                }
            },
        'autocdata': (),
        'autoclose_all': False,
        'autoclose_end': '>',
        'autocdata_enabled': False,
        }
    html5_overrides = dict(
        html4_overrides,
        default_attributes={},
        )
    xhtml_overrides = {
        'default_attributes': dict(
            html4_overrides['default_attributes'],
            html={
                '.xmlns': 'http://www.w3.org/1999/xhtml',
                '.xml:lang': 'en',
                '.lang': 'en',
                },
            ),
        'autocdata': ('style', 'script'),
        'autoclose_all': True,
        'autoclose_end': '/>',
        'autocdata_enabled': True,
        }
    doctypes = {
        'html4-strict': (
            '<!DOCTYPE HTML'
            ' PUBLIC "-//W3C//DTD HTML 4.01//EN"'
            ' "http://www.w3.org/TR/html4/strict.dtd">',
            html4_overrides,
            ),
        'html4-transitional': (
            '<!DOCTYPE HTML'
            ' PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"'
            ' "http://www.w3.org/TR/html4/loose.dtd">',
            html4_overrides,
            ),
        'html4-frameset': (
            '<!DOCTYPE HTML'
            ' PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN"'
            ' "http://www.w3.org/TR/html4/frameset.dtd">',
            html4_overrides,
            ),
        'html5': (
            '<!DOCTYPE html>',
            html5_overrides,
            ),
        'xhtml1-strict': (
            '<!DOCTYPE html'
            ' PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"'
            ' "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">',
            xhtml_overrides,
            ),
        'xhtml1-transitional': (
            '<!DOCTYPE html'
            ' PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"'
            ' "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">',
            xhtml_overrides,
            ),
        'xhtml1-frameset': (
            '<!DOCTYPE html'
            ' PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN"'
            ' "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">',
            xhtml_overrides,
            ),
        'xhtml11': (
            '<!DOCTYPE html'
            ' PUBLIC "-//W3C//DTD XHTML 1.1//EN"'
            ' "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">',
            xhtml_overrides,
            ),
        }

    def _map_value(self, name, value, handler, prefer_value, sep=' '):
        if value in self.empty_values:
            pass
        elif self._is_nonstr_iterable(value):
            start = None
            for txt, _, start in self._map_pairs(value, handler, prefer_value):
                yield ('{}="{}'.format(name, txt) if start else '{}{}'.format(
                    sep, txt))
            if start is not None:
                yield '"'
        else:
            yield '{}="{}"'.format(name, value)

    def node_doctype(self, name, value):
        if value in self.doctypes:
            header, overrides = self.doctypes[value]
            for attr, value in overrides.items():
                setattr(self, attr, value)
            self.doctype = value
            yield '{}\n'.format(header)

    def attr_style(self, name, value):
        for txt in self._map_value(name, value, self.value_style, False, ';'):
            yield txt

    def attr_class(self, name, value):
        for txt in self._map_value(name, value, self.value_class, True, ' '):
            yield txt

    def value_style(self, name, value):
        if value in self.empty_values:
            yield '{}:none'.format(name)
        elif self._is_nonstr_iterable(value):
            pairs = self._map_pairs(value, self.value_style)
            for txt, first_value, first_pair in pairs:
                yield '{}-{}'.format(name, txt) if first_value else txt
        else:
            yield '{}:{}'.format(name, value)

    def value_class(self, name, value):
        if value in self.empty_values:
            yield name
        elif self._is_nonstr_iterable(value):
            pairs = self._map_pairs(value, self.value_class, True)
            for txt, first_value, first_pair in pairs:
                if first_value and name:
                    yield '{}-{}'.format(name, txt) if txt else name
                else:
                    yield txt
        else:
            yield '{}-{}'.format(name, value) if name else value
