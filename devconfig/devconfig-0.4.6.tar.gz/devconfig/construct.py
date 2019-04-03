import os
import sys
from functools import partial as _partial, lru_cache
import importlib._bootstrap_external
from importlib.util import find_spec
from importlib import invalidate_caches, import_module
import logging
import locale
from pathlib import Path
from contextlib import contextmanager
import yaml.nodes
import yaml.constructor
import yaml.resolver
import attr
import devconfig
import devconfig.merge

import pkg_resources

_log = logging.getLogger(__name__)

def envvar(loader, delimiter, node):
    varname = delimiter[delimiter.index(':') + 1:]
    if isinstance(node, yaml.nodes.MappingNode):
        envvar_config = loader.construct_mapping(node)
    elif isinstance(node, yaml.nodes.ScalarNode):
        envvar_config = {}
    else:
        raise yaml.constructor.ConstructorError('unknown !envvar format')

    construct = _partial(envvar_config.get('constructor', lambda x:x))
    if 'default' in envvar_config:
        return construct(os.environ.get(varname, envvar_config['default']))
    else:
        return construct(os.environ[varname])


def yaml_file_finder(cls, extensions):
    current_loaders = importlib._bootstrap_external._get_supported_file_loaders()
    current_loaders.append((cls, extensions))
    sys.path_hooks[-1] = importlib.machinery.FileFinder.path_hook(*current_loaders)
    invalidate_caches()
    for name in [name for name in sys.path_importer_cache]:
        del sys.path_importer_cache[name]


def module_extend(loader, delimiter, node):
    extended_module_name = node.tag.rsplit(':', 1)[-1].strip()
    _log.debug(loader.module['spec']['name'],
                extra={ 'extends': extended_module_name,
                        'spec': loader.module})
    if not extended_module_name:
        return loader.construct_mapping(node, deep=True)

    if extended_module_name in sys.modules:
        extended_module_mapping = dict(
            ((k,v) for (k,v) in sys.modules[extended_module_name].__dict__.items() 
                 if not k.startswith('__')))
        return devconfig.merge.mappings(loader.construct_mapping(node, deep=True), extended_module_mapping)
    else:
        extended_module_spec = find_spec(extended_module_name)
        if extended_module_spec is None:
            return loader.construct_mapping(node, deep=True)

        extended_module_path = extended_module_spec.origin
        with open(extended_module_path) as stream:
            extended_module_node = next(devconfig.documents(stream))
            devconfig.merge.extend_node(node, extended_module_node)
        return loader.construct_object(extended_module_node, deep=True)

IMPLICIT_RESOLVER = {}

def implicit_resolver(loader, node, name='_'):
    resolver = loader.construct_mapping(node, deep=True)
    if name == '_':
        loader.add_implicit_resolver(**resolver)
    else:
        IMPLICIT_RESOLVER_SETS[name] = resolver
    return resolver


KIND = {
    'mapping': dict,
    'sequence': list,
    'scalar': str,
    None: None,
    '': None
}

@attr.s
class PathObject:
    tag = attr.ib(converter=lambda value: value.lstrip('.'))
    kind = attr.ib(default=None)

@attr.s
class PathResolver:
    object = attr.ib(default=[])
    node = attr.ib(default=[])
    @classmethod
    def construct(cls, loader, _node):
        if _node.tag.startswith('!resolver:'):
            return loader.construct_object(_node)
        assert isinstance(_node, yaml.nodes.MappingNode), 'PathResolver configuration should be a mapping'
        object = []
        node = []
        merged = []
        for node_check_key_yaml_node, node_check_value_yaml_node in _node.value:
            node_check_key = loader.construct_scalar(node_check_key_yaml_node)
            if node_check_key.startswith('.'):
                node_check_value = loader.construct_scalar(node_check_value_yaml_node)
                object.append(PathObject(node_check_key, KIND[node_check_value]))
            elif node_check_key.startswith('~'):
                loader.construct_object(node_check_value_yaml_node)
            elif node_check_key in KIND:
                for index_check_key_yaml_node, index_check_value_yaml_node in node_check_value_yaml_node.value:
                    index_check_key = loader.construct_object(index_check_key_yaml_node)
                    node.append(((KIND[node_check_key], index_check_key), cls.construct(loader, index_check_value_yaml_node)))
            elif node_check_key == '<<':
                merged.append(loader.construct_object(node_check_value_yaml_node))
            else:
                raise yaml.constructor.ConstructorError(f'PathResolver keys should either start with ["." | "~" | "<<"] or be in range {KIND.keys()}')
        for merge in merged:
            object.extend(merge.object)
            node.extend(merge.node)
        return cls(object, node)

    def __call__(self):
        for path_object in self.object:
            yield (), path_object

        for subpath, subresolver in self.node:
            for suffix, path_object in subresolver():
                yield (subpath,) + suffix, path_object

PATH_RESOLVER = {}

def set_path_resolver(loader, node, name='_'):
    resolver = PathResolver.construct(loader, node)
    if name == '_':
        append_path_resolvers(loader, resolver)
    else:
        PATH_RESOLVER[name] = resolver

def append_path_resolvers(loader, resolver):
    for path, path_object in resolver():
        loader.add_path_resolver(path_object.tag, path, kind=path_object.kind)

def get_path_resolver(loader, node, name='_'):
    return PATH_RESOLVER[name]


DEFAULT_STRJOIN_DELIMITER = ''

def strjoin_from_mapping(loader, nodes, default_delimiter=DEFAULT_STRJOIN_DELIMITER):
    joined = []
    for node in nodes.value:
        if isinstance(node[1], yaml.nodes.SequenceNode):
            joined.extend(loader.construct_object(node[1]))

    delimiter = loader.construct_mapping(nodes).get('delimiter', default_delimiter)
    return delimiter.join(str(i) for i in joined)

def strjoin_from_sequence(loader, items, delimiter, default_delimiter=DEFAULT_STRJOIN_DELIMITER):
    if not delimiter:
        delimiter = default_delimiter
    elif delimiter == ':':
        delimiter = ' '
    else:
        delimiter = delimiter[1:] if delimiter[0] == ':' else delimiter
    items = loader.construct_sequence(items)
    return str(delimiter).join(str(i) for i in items)

def strjoin(loader, delimiter, node):
    if isinstance(node, yaml.nodes.SequenceNode):
        return strjoin_from_sequence(loader, node, delimiter)
    elif isinstance(node, yaml.nodes.MappingNode):
        return strjoin_from_mapping(loader, node)
    raise yaml.constructor.ConstructorError('attempt to !strjoin on node with unknown layout')


DEFAULT_FILE_ENCODING = locale.getpreferredencoding(False)

def file_contents(loader, coding, node, default_coding=DEFAULT_FILE_ENCODING):
    if not coding or coding==':':
        coding = default_coding
    else:
        coding = coding[1:] if coding[0] == ':' else coding

    with io.open(loader.construct_object(node), encoding=coding) as file_contents:
        return file_contents.read()


def asset(loader, node):
    _path = Path(pkg_resources.resource_filename(loader.module['package'], '')).resolve()
    if isinstance(node, yaml.nodes.ScalarNode):
        return _path / loader.construct_scalar(node)
    elif isinstance(node, yaml.nodes.SequenceNode):
        for _sub in loader.construct_sequence(node):
            _path = _path / _sub
        return _path
    else:
        raise yaml.constructor.ConstructorError('unknown !path format')


def partial(loader, node):
    config = loader.construct_mapping(node, deep=True)
    return _partial(config['callable'], *config.get('args', ()), **config.get('kwargs', {}))


def path(loader, delimiter, node):
    if not delimiter or delimiter == ':':
        _root = ''
    else:
        _root = delimiter[1:] if delimiter[0] == ':' else delimiter
    _path = Path(_root)
    
    if isinstance(node, yaml.nodes.ScalarNode):
        return _path / loader.construct_scalar(node)
    elif isinstance(node, yaml.nodes.SequenceNode):
        for _sub in loader.construct_sequence(node):
            _path = _path / _sub
        return _path
    else:
        raise yaml.constructor.ConstructorError('unknown !path format')
path.__doc__ = Path.__doc__


def dir(loader, delimiter, node):
    _path = path(loader, delimiter, node)
    _current = Path('.').resolve()
    @contextmanager
    def _dir(create=False, exist_ok=False):
        if create:
            os.makedirs(_path, exist_ok=exist_ok)
        os.chdir(_path)
        try:
            yield _path
        finally:
            os.chdir(_current)
    _dir._current = _current
    _dir._path = _path
    return _dir


@lru_cache(maxsize=1)
def render_globals():
    merges = [dict([(k,v) for k,v in __builtins__.items() if not k.startswith('__')])]
    for devconfig_ep in pkg_resources.iter_entry_points('devconfig'):
        if devconfig_ep.name == 'namespace':
            mod_dict = import_module(devconfig_ep.module_name).__dict__
            merges.append(dict([(k, v) for k,v in mod_dict.items() if not k.startswith('__')]))
    return devconfig.merge.mappings(*merges)

def fstring_callable(loader, node, namespace=None):
    f = loader.construct_scalar(node)
    if namespace is None:
        _locals = {}
    else:
        _locals = construct_shadow_object(loader, namespace)

    return _partial(eval, f'''f"{f}"''', devconfig.merge.mappings(render_globals(), _locals))

def fstring_rendered(loader, node, namespace=None):
    return fstring_callable(loader, node, namespace=namespace)({'__namespace': str(namespace)})

class ShadowConstructor(yaml.constructor.Constructor, yaml.resolver.Resolver):
    NODETAG = (
            (yaml.nodes.MappingNode, 'tag:yaml.org,2002:map'),
            (yaml.nodes.SequenceNode, 'tag:yaml.org,2002:seq'),
        )

    def __init__(self):
        yaml.constructor.Constructor.__init__(self)
        yaml.resolver.Resolver.__init__(self)

    def construct_object(self, node, deep=False):
        _initial_tag = None
        if (node.tag not in self.yaml_constructors) and (''.join(node.tag.rpartition(':')[:-1]) not in self.yaml_multi_constructors):
            if isinstance(node, yaml.nodes.ScalarNode):
                return super().construct_scalar(node)
            else:
                for _nodetype, _nodetag in self.NODETAG:
                    if isinstance(node, _nodetype):
                        initial = node.tag
                        node.tag = _nodetag
                        try:
                            return super().construct_object(node, deep=deep)
                        finally:
                            node.tag = initial
        else:
            return super().construct_object(node, deep=deep)


def construct_shadow_object(loader, namespace):
    loader.__dict__.setdefault('shadow_namespace_object', {})
    if namespace in loader.shadow_namespace_object:
        return loader.shadow_namespace_object[namespace]
    loader.shadow_namespace_object[namespace] = ShadowConstructor().construct_object(loader.collected_namespace_node[namespace],
                                                                                     deep=True)
    del loader.collected_namespace_node[namespace]
    return loader.shadow_namespace_object[namespace]


def attributed_object(loader, node, classname=None):
    return loader.find_python_name(classname, node.start_mark).from_yaml_node(loader, node)

def merged(loader, node):
    return devconfig.merge.mappings(*loader.construct_sequence(node))
merged.__doc__ = devconfig.merge.mappings.__doc__


def getattribute(loader, delimiter, node):
    if not delimiter.startswith(':'):
        raise yaml.constructor.ConstructorError('unknown !getattribute format')
    else:
        delimiter = delimiter[1:]
    attr_name = loader.construct_scalar(node)
    node.value = None
    return getattr(loader.construct_python_name(delimiter, node), attr_name)


def class_(loader, node, name='UnnamedClass', base=None):
    bases=[]
    members = {}
    if base:
        bases.append(loader.find_python_name(base, node.start_mark))
    if isinstance(node, yaml.nodes.SequenceNode):
        for base in loader.construct_sequence(node):
            bases.append(base)
    elif isinstance(node, yaml.nodes.MappingNode):
        members = loader.construct_mapping(node, deep=True)
    if hasattr(loader, 'module'):
        members['__module__'] = loader.module['spec']['name']
    return type(name, tuple(bases), members)
