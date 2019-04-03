import yaml
from yaml.nodes import *
import yaml.constructor
import yaml.composer
import attr
import logging
import pkg_resources
from pathlib import Path
from operator import attrgetter
from functools import partial, wraps
from importlib.util import find_spec
from collections.abc import Mapping, Sequence
import sys

from collections import namedtuple
import attr


_log = logging.getLogger(__name__)

DEVCONFIG_NAMESPACE = "!tag:devconfig:"

class DevconfigLoader(yaml.Loader):
    extensions = []
    def compose_mapping_node(self, anchor):
        node = super().compose_mapping_node(anchor)
        if anchor:
            self.__dict__.setdefault('collected_namespace_node', {}).update({anchor: node})
        return node

attrs_logdict = partial(attr.asdict, filter=lambda attr,value: attr.name != 'name')


class YAMLObjectDeclarationBaseAttributesMixin(object):
    UNDEFINED = object()
    def attrdict(self):
        return dict((k,v) for
                    (k,v) in self._asdict().items()
                    if not v==self.UNDEFINED)

def _yaml_object_declaration_attributes(attrs):
    if sys.version_info.minor >= 7:
        return type('DeclaredConstructorAttributes', (namedtuple('AttributesTuple',
                                              attrs,
                                              defaults=(YAMLObjectDeclarationBaseAttributesMixin.UNDEFINED,) * len(attrs)),
                                   YAMLObjectDeclarationBaseAttributesMixin), {})
    else:
        base = namedtuple('AttributesTuple', attrs)
        base.__new__.__defaults___ = (YAMLObjectDeclarationBaseAttributesMixin.UNDEFINED,) * len(attrs)
        return type('DeclaredConstructorAttributes', (base, YAMLObjectDeclarationBaseAttributesMixin), {})

@attr.s(kw_only=True)
class YAMLObjectDeclarationBase(object):
    yaml_loader = DevconfigLoader
    handler = attr.ib()
    tag = attr.ib()
    attributes = attr.ib(converter=_yaml_object_declaration_attributes,
                         default=[])
    def __setstate__(self, state):
        if isinstance(state, Mapping):
            self.__init__(**state)
        elif isinstance(state, Sequence):
            self.__init__(*state)
        else:
            self.__init__(state)


@attr.s(kw_only=True)
class SingleConstructorDeclaration(yaml.YAMLObject, YAMLObjectDeclarationBase):
    yaml_tag = f'{DEVCONFIG_NAMESPACE}extend/with/constructor/single'
    def __attrs_post_init__(self):
        context.loader.add_constructor(self.tag, self.handler)
        _log.debug(f'declare', extra=dict(loader=context.loader, **attrs_logdict(self)))


@attr.s(kw_only=True)
class MultiConstructorDeclaration(yaml.YAMLObject, YAMLObjectDeclarationBase):
    yaml_tag = f'{DEVCONFIG_NAMESPACE}extend/with/constructor/multi'
    def parsed_attributes(self, handler):
        @wraps(handler)
        def _handler(loader, attributes, node):
            attrdict = self.attributes(*(attributes.split(':') if attributes else ())).attrdict()
            for attrname in list(attrdict.keys()):
                if attrdict[attrname] == attrname:
                    attrdict[attrname] = 'true'
                elif attrdict[attrname] == f'no-{attrname}':
                    attrdict[attrname] = 'false'
                attrdict[attrname] = yaml.load(attrdict[attrname])
            return handler(loader, node, **attrdict)
        return _handler

    def __attrs_post_init__(self):
        if self.attributes._fields:
            handler = self.parsed_attributes(self.handler)
        else:
            handler = self.handler
        context.loader.add_multi_constructor(self.tag, handler)
        _log.debug(f'declare', extra=dict(loader=context.loader, **attrs_logdict(self)))


@attr.s(kw_only=True)
class YAMLObjectDeclaration(yaml.YAMLObject, YAMLObjectDeclarationBase):
    yaml_tag = f'{DEVCONFIG_NAMESPACE}extend/with/object'
    name = attr.ib()
    result = attr.ib(default=None)
    def __attrs_post_init__(self):
        class YAMLObjectMixin(object):
            def __setstate__(_self, state):
                _self.__init__(**state)
            def __attrs_post_init__(_self):
                self.result = self.handler(**attr.asdict(_self))
                _log.debug(f'handled', extra=dict(yaml_tag=self.tag, **attrs_logdict(self)))

        YAMLObjectAttributes = attr.make_class(self.name+'Attributes',
                                               dict(((k, attr.ib(kw_only=True)) for k in self.attributes._fields)))
        attr.s(yaml.YAMLObjectMetaclass(self.name,
                (yaml.YAMLObject, YAMLObjectAttributes, YAMLObjectMixin),
                {'yaml_tag': self.tag, 'yaml_loader': context.loader}))
        _log.debug(f'declare',  extra=attrs_logdict(self))


class _LoaderContext(object):
    stacked_attr_names = [
        'yaml_constructors',
        'yaml_multi_constructors',
        'yaml_implicit_resolvers',
        'yaml_path_resolvers',
        'extensions',
    ]
    stack = []
    @classmethod
    def push(self, name='NestedDevconfigLoader', base=None, method_funcs={}):
        depth = len(self.stack)
        assert base or depth, 'Initial push must be called with yaml.Loader subclass as base'
        if not depth:
            bases = (base,)
            _cls = type(f'{name}_depth_{depth}', bases, {})
            for method_name, method_func in method_funcs.items():
                setattr(_cls, method_name, method_func.__get__(None, _cls))
        else:
            bases = (self.stack[-1],)
            _cls = type(f'{name}_depth_{depth}', bases, {})

        for stacked_attr_name in self.stacked_attr_names:
            setattr(_cls, stacked_attr_name, getattr(bases[0], stacked_attr_name).copy())

        self.stack.append(_cls)
        return self.stack[-1]

    @classmethod
    def pop(self):
        return self.stack.pop()

    @property
    def loader(self):
        return self.stack[-1]

context = _LoaderContext()


context.push(base=DevconfigLoader)


def documents(stream, loader=None):
    if loader is None:
        loader = context.loader(stream)
    while loader.check_node():
        document = loader.get_node()
        try:
            if document.tag.startswith(f'{DEVCONFIG_NAMESPACE}extend'):
                loader.extensions.append(loader.construct_document(document))
            else:
                document.loader = loader
                yield document
        except yaml.constructor.ConstructorError as e:
            _log.exception(e)


for devconfig_ep in pkg_resources.iter_entry_points(__name__):
    if devconfig_ep.name == 'extend':
        for extend_name in devconfig_ep.extras:
            with open(Path(find_spec(devconfig_ep.module_name).origin).parent / extend_name) as extension:
                list(documents(extension))

