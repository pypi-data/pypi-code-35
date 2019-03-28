from . import base


class XMLProcessError(base.ProcessError):
    pass


class AttributeExtractor(object):
    def __init__(self, iterable, is_attr, defaults={}):
        self.is_attr = is_attr
        self.iterable = iter(iterable)
        self.defaults = defaults

    def attributes(self):
        attr_names = set()
        for attr, value in self.iterable:
            if not self.is_attr(attr):
                # recreate iterable to prepend consumed item
                self.iterable = (
                    item
                    for src in ([(attr, value)], self.iterable)
                    for item in src
                    )
                break
            attr_names.add(attr)
            yield attr, value

        for attr, value in self.defaults.items():
            if attr not in attr_names:
                yield attr, value

    def remaining(self):
        first = True
        for name, value in self.iterable:
            if first and self.is_attr(name):
                raise RuntimeError('Attribute generator not exhausted')
            yield name, value
            first = False


class XMLProcessor(base.BaseProcessor):
    exc_class = XMLProcessError
    attrextractor_class = AttributeExtractor
    default_attributes = {}
    empty_values = ('', None)
    autocdata = ()
    autoclose = ()
    autoclose_all = True
    autoclose_end = '/>'
    text_escapes = (
        ('&', '&amp;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
        )
    value_escapes = (
        ('&', '&amp;'),
        ('"', '&quot;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
        )
    config = {
        'attr_prefix': '.',
        'text_node': '.text',
        'cdata_node': '.cdata',
        'literal_node': '.literal',
        }
    nodes = {
        '.text': 'custom_text',
        '.cdata': 'custom_cdata',
        '.literal': 'custom_literal',
        '.comment': 'custom_comment',
        }
    attrs = {}

    def __init__(self, tree):
        super(XMLProcessor, self).__init__(tree)

        # update dict nodes and attrs to receive self
        self.default_attributes = dict(self.default_attributes)
        self.nodes = {k: getattr(self, v) for k, v in self.nodes.items()}
        self.attrs = {k: getattr(self, v) for k, v in self.attrs.items()}

    @classmethod
    def _preprocess_pair(cls, item, prefer_value=False):
        if cls._is_nonstr_iterable(item):
            try:
                sn, sv = item
            except (TypeError, ValueError):
                sn, sv = (None, item) if prefer_value else (item, None)
        else:
            sn, sv = (None, item) if prefer_value else (item, None)
        return sn, sv

    @classmethod
    def _map_pairs(cls, pairs, handler, enforce_index=-1):
        first_pair = True
        for item in pairs:
            sn, sv = cls._preprocess_pair(item, enforce_index)
            first_value = True
            for data in handler(sn, sv):
                yield data, first_value, first_pair
                first_value = False
                first_pair = False

    def is_attr(self, name):
        attr_prefix = self.config['attr_prefix']
        return name.startswith(attr_prefix) and name not in self.nodes

    def extract_node_attributes(self, name, value):
        defaults = self.default_attributes.get(name, {})
        if self._is_nonstr_iterable(value):
            extractor = self.attrextractor_class(value, self.is_attr, defaults)
            return extractor.attributes(), extractor.remaining()
        return defaults.items(), [(self.config['text_node'], value)]

    def escape_text(self, value):
        for char, escape in self.text_escapes:
            value = value.replace(char, escape)
        return value

    def escape_value(self, value):
        for char, escape in self.value_escapes:
            value = value.replace(char, escape)
        return value

    def process_attr(self, name, value, root=False):
        if root:
            name = name[len(self.config['attr_prefix']):]
        if name in self.attrs:
            return self.attrs[name](name, value)
        return self.default_attr(name, value)

    def process_node(self, name, value):
        if name in self.nodes:
            return self.nodes[name](name, value)
        if name.startswith(self.config['attr_prefix']):
            raise self.exc_class('Unexpected node attr %r' % name)
        return self.default_node(name, value)

    def default_attr(self, name, value):
        if value in self.empty_values:
            yield name
        elif self._is_nonstr_iterable(value):
            for txt, first, start in self._map_pairs(value, self.process_attr):
                yield (
                    '{}-{}'.format(name, txt) if start else
                    ' {}-{}'.format(name, txt) if first else
                    txt
                    )
        else:
            yield '{}="{}"'.format(name, self.escape_value(value))

    def default_node(self, name, value):
        yield '<{}'.format(name)

        attrs, value = self.extract_node_attributes(name, value)
        for attr, aval in attrs:
            first = True
            for txt in self.process_attr(attr, aval, True):
                yield ' {}'.format(txt) if first else txt
                first = False

        if name in self.autocdata:
            value = [(self.config['cdata_node'], value)]

        first = True
        for txt in self.process_value(value):
            yield '>{}'.format(txt) if first else txt
            first = False

        yield (
            '</{}>'.format(name)
            if not first else
            self.autoclose_end
            if self.autoclose_all or name in self.autoclose else
            '></{}>'.format(name)
            )

    def custom_comment(self, name, value):
        first = True
        for txt in self.process_value(value):
            yield '<!-- {}'.format(txt) if first else txt
            first = False
        yield '<!-- -->' if first else ' -->'

    def custom_cdata(self, name, value):
        text_node = self.config['text_node']
        text_node_handler = self.nodes[text_node]
        self.nodes[text_node] = self.nodes[self.config['literal_node']]

        first = True
        for txt in self.process_value(value):
            yield '<![CDATA[{}'.format(txt) if first else txt
            first = False

        if not first:
            yield ']]>'

        self.nodes[text_node] = text_node_handler

    def custom_text(self, name, value):
        if value in self.empty_values:
            return
        yield '{}'.format(self.escape_text(value))

    def custom_literal(self, name, value):
        yield '{}'.format(value)
