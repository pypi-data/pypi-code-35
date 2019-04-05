"""Specular specification toolkit.

Specify, configure, and construct objects using documents.

"""

from collections import Mapping, Sequence, defaultdict
from pprint import pformat
from itertools import chain, izip
from types import FunctionType
from inspect import getargspec
import traceback
import sys
from random import choice, randint
import re
import importlib


Bytes = str
Text = unicode
Omit = object()


def iter_spec_artifacts(context, path=(), missing=Omit, keys=False):
    spec = context['spec']
    subspec = spec.getpath(path)
    subloc = context['loc'] + path
    artifacts = context['artifacts']
    for key, _ in subspec.iter_level_values():
        artifact_key = subloc + (key,)
        try:
            value = artifacts[artifact_key]
        except KeyError:
            if missing is not Omit:
                value = missing
            else:
                continue
        yield (key, value) if keys else value


def doc_locate(doc, path):
    """Walk a path down a document.

    The path is a list of bytestring segments.
    Starting from the root node, a cursor points at the first segment.

    At each node, the segment under the cursor is used
    to access the node to go deeper.

    As the cursor moves from the begining towards the end of the segment list,
    the list is logically split into two parts.

    The first part, the trail, is the prefix of segments
    that have already been used in descending through the document hierarchy
    and corresponds to the current path.

    The second part of the path, the feed, is the suffix of segments
    that have not yet been accessed to descend to the full path.

    There are two outcomes:
        1. feed is empty, meaning that the given path was found
        2. feed is non-empty, meaning that the first segment in the feed was
           not found in the document at the path formed by the trail.

    Args:
        doc (dict):
            A recursive object-document
        path (tuple):
            A sequence of path segments as in ('path', 'to', 'somewhere')

    Returns:
        tuple of lists:
            feed (list):
                List of path segments left that have not yet been accessed
            trail (list):
                List of path segments already accessed. It corresponds to the
                current path of the node where no further descent was possible
                and thus doc_locate() was terminated.
            nodes (list):
                List of nodes already accessed, in order.
    """
    feed = list(reversed(path))
    trail = []
    nodes = [doc]
    while feed:
        segment = feed.pop()
        if not segment:
            continue

        if not isinstance(doc, dict) or segment not in doc:
            feed.append(segment)
            break

        trail.append(segment)
        doc = doc[segment]
        nodes.append(doc)

    return feed, trail, nodes


def doc_set(doc, path, value, multival=False):
    if not path:
        return value

    feed, trail, nodes = doc_locate(doc, path)

    doc = nodes[-1]
    if feed and isinstance(doc, dict):
        # path was not found and parent points to a sub-doc
        doc = nodes[-1]
        while True:
            segment = feed.pop()
            if not feed:
                break
            new_doc = {}
            doc[segment] = new_doc
            doc = new_doc

        doc[segment] = value
        old_value = None

    else:
        # path was found or stopped in a scalar value, we have to replace the
        # last node with a hierarchy from feed
        parent = nodes[-2]
        segment = trail[-1]
        old_value = parent[segment]
        new_value = value
        for key in feed:
            new_value = {key: new_value}
        if not multival:
            parent[segment] = new_value
        elif hasattr(old_value, 'append'):
            old_value.append(new_value)
        else:
            parent[segment] = [old_value, new_value]

    return old_value


def doc_get(doc, path):
    feed, trail, nodes = doc_locate(doc, path)
    return None if feed else nodes[-1]


def doc_merge(doca, docb, merge=None):
    docout = {}

    keys = set(doca.keys())
    keys.update(docb.keys())

    for key in keys:
        vala = doca.get(key)
        valb = docb.get(key)

        if isinstance(vala, dict) and isinstance(valb, dict):
            doc = doc_merge(vala, valb, merge=merge)
            if doc:
                docout[key] = doc
        else:
            if merge:
                val = merge(vala, valb)
            else:
                val = valb
            if val is not None:
                docout[key] = val

    return docout


def doc_iter(doc, preorder=None, postorder=None, path=(),
             ordered=False, multival=False):

    """Iterate the document hierarchy yielding each path and node.

    Args:

        doc (dict):
            A hierarchical object-document

        preorder (bool):
            If true, yield path and node at the first node visit.

        postorder (bool):
            If true, yield path and node at the second node visit.

            Note that postorder is independent from preorder.
            If both are true, nodes will be yielded two times.
            If none is true, doc is iterated for any possible side-effects,
            but nothing is yielded.

            If no preorder or postorder is given,
            then postorder defaults to True and preorder to False.
            Otherwise, if preorder or postorder is false,
            then the other defaults to True.

        path (tuple):
            A prefix path to append in yielded paths

        ordered (bool):
            If keys within a node will be visited in a sorted order or not.

        multival:
            When true, lists, tuples, and sets are entered as subdocuments.
            Their elements are enumerated and their index is appended in the
            path as elem(long)

    Yields:

        tuple of (path, node):
            path (tuple):
                The segments of the current path
            node (dict):
                The node at the current path.

    Receives:

        None or True:
            If None is received, iteration continues normally.
            If True is received, iteration skips current node.
            Note that skip only works if preorder=True, otherwise
            there will be no chance to send True before the nod
            children are visited.
    """
    skip = None

    if preorder is None:
        if postorder is None:
            postorder = True
        elif not postorder:
            preorder = True
    elif not preorder and postorder is None:
        postorder = True

    if preorder:
        skip = (yield path, doc)

    if not skip:
        doc_type = type(doc)
        if multival and doc_type in (list, tuple, set):
            for i, val in enumerate(doc):
                subpath = path + (elem(i),)
                g = doc_iter(val,
                             preorder=preorder, postorder=postorder,
                             path=subpath, multival=multival)
                try:
                    skip = None
                    while True:
                        skip = yield g.send(skip)
                except StopIteration:
                    pass

        elif doc_type is dict:
            iteritems = sorted(doc.iteritems()) if ordered else doc.iteritems()
            for key, val in iteritems:
                subpath = path + (key,)
                g = doc_iter(val,
                             preorder=preorder, postorder=postorder,
                             path=subpath, multival=multival)
                try:
                    skip = None
                    while True:
                        skip = yield g.send(skip)
                except StopIteration:
                    pass

    if postorder:
        yield path, doc


class Error(Exception):

    message = ''
    errs = ()
    loc = ()
    codeloc = ''
    what = ''

    def __init__(self, message=None, what='', loc=(), errs=(), **kwargs):
        self.message = message
        self.errs = errs
        self.what = what
        self.loc = loc
        self.codeloc = ':'.join(str(x) for x in traceback.extract_stack()[-2])
        self.kwargs = kwargs

    def to_dict(self):
        args = {}
        args.update(self.kwargs)
        args['Code'] = self.codeloc
        args['Errors'] = [
            x.to_dict() if hasattr(x, 'to_dict') else repr(x)
            for x in self.errs
        ]
        args['Location'] = self.loc
        args['Message'] = self.message
        args['What'] = self.what
        return args

    def to_string(self, depth=1):
        return pformat(self.to_dict(), indent=2, width=120)

    def __repr__(self):
        return self.to_string()

    __str__ = __repr__


def collect_error(errs, exc):
    errs.append(exc)


NULL = type(
    'NULL',
    (),
    {
        '__repr__': lambda _: 'NULL',
        '__nonzero__': lambda _: False,
    },
)()


def key_to_path(key):
    return tuple(iter_key_to_path(key))


def iter_key_to_path(key):

    if not key:
        return

    if '/' in key:
        segments = key.split('/')

    else:
        for sep in '.?':
            if sep not in key:
                continue

            pf, _, sf = key.partition(sep)
            if pf:
                yield pf
            yield sep
            segments = sf.split(sep)
            break
        else:
            segments = (key,)

    if not segments[-1]:
        del segments[-1]

    for segment in segments:
        yield segment


def path_to_key(path):
    return b'/'.join(path)


def getpath(spec, path=()):

    for segment in path:
        if spec is NULL or spec is ANY or spec.__class__ is not Spec:
            spec = NULL
            break

        nodes = spec.nodes
        if segment not in nodes:
            return NULL
        else:
            spec = nodes[segment]

    return spec


def merge_source(target, source, loc=()):
    for key in source:
        if key not in target:
            target[key] = source[key]
            continue

        target_val = target[key]
        source_val = source[key]

        if (
            target_val.__class__ is not Source and
            source_val.__class__ is not Source
        ):

            if target_val == source_val:
                continue

            m = "value mismatch"
            e = Error(what='cannot-normalize', loc=loc)
            raise e

        elif (
            target_val.__class__ is Source and
            source_val.__class__ is Source
        ):

            loc = loc + (key,)
            merge_source(target_val, source_val, loc=loc)

        else:
            m = "sources not normalized"
            raise AssertionError(m)


class Source(dict):
    __slots__ = ()


class Data(object):

    __slots__ = ('value',)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Data({0!r})".format(self.value)


def normalize_source(doc):

    if doc.__class__ is Source:
        return doc

    newdoc = Source()

    if isinstance(doc, (Bytes, Text)):
        newdoc[b'='] = doc
        return newdoc
    elif isinstance(doc, Sequence):
        z = len("%d" % len(doc))
        doc = {'%0*d' % (z, i): v for i, v in enumerate(doc)}
    elif isinstance(doc, Data):
        newdoc[b'='] = doc.value
        return newdoc
    elif not isinstance(doc, Mapping):
        newdoc[b'='] = doc
        return newdoc

    for key in sorted(doc):
        subdoc = doc[key]
        if key.__class__ is not str:
            key = key.encode('utf-8')

        if key == b'=':
            newdoc[b'='] = doc[b'=']
            continue

        path = key_to_path(key)
        curdoc = newdoc

        for segment in path:
            if segment == b'=':
                m = "cannot use '=' as a source path segment"
                raise Error(what='invalid', message=m)

            if segment not in curdoc:
                curdoc[segment] = Source()

            curdoc = curdoc[segment]

        subdoc = normalize_source(subdoc)
        merge_source(curdoc, subdoc, loc=path)

    return newdoc


def setval(spec, path, value):

    target_spec = spec
    iter_path = iter(path)
    for segment in iter_path:
        if segment in target_spec.nodes:
            new_spec = target_spec.nodes[segment]
        elif target_spec.nodes:
            new_spec = Spec()
            target_spec.nodes[segment] = new_spec
        else:
            new_spec = Spec()
            target_spec.nodes = {segment: new_spec}
        target_spec = new_spec

    oldval = target_spec.value
    target_spec.value = value

    return oldval


class DeferConstructor(Exception):
    """An exception raised by constructors to defer their execution."""


class SkipConstructor(Exception):
    """An exception raised by constructors to skip their execution."""


cons_context_fields = frozenset((
    'spec',
    'loc',
    'top_spec',
    'constructions',
    'construction',
    'constructors',
    'value',
    'output',
    'artifacts',
    'global_artifacts',
    'settings',
    'dependencies',
    'schemata',
    'constructed',
    'skipped',
    'round',
    'errs',
    'predicate',
    'args',
))


def make_constructor(constructor):
    if isinstance(constructor, FunctionType):
        fn = constructor
        fn_module = constructor.__module__
        args = getargspec(fn).args
        fn_name = constructor.func_name
    elif callable(constructor) and hasattr(constructor, '__call__'):
        fn = constructor.__call__
        args = getargspec(fn).args[1:]
        fn_name = constructor.__class__.__name__
        fn_module = constructor.__call__.__module__
    else:
        m = "{constructor!r}: not a FunctionType or callable"
        m = m.format(constructor=constructor)
        raise Error(what='invalid', message=m)

    if args == ['context']:
        return constructor

    unknown_args = set(args) - cons_context_fields
    unknown_args.discard('context')

    if unknown_args:
        m = ("{name!r}: unknown constructor arguments: {unknown_args!r}. "
             "the available context fields are {cons_context_fields!r}.")
        m = m.format(name=fn_module + b'.' + fn_name,
                     unknown_args=list(unknown_args),
                     cons_context_fields=cons_context_fields)
        raise Error(what='invalid', message=m)

    def final_constructor(context):
        kwargs = {name: context[name] for name in args}
        if 'context' in kwargs:
            kwargs['context'] = context
        return fn(**kwargs)

    final_constructor.func_name = fn_name
    return final_constructor


def construct_after(context, *predicates):
    processed = context['constructed'] | context['skipped']
    if len(processed.intersection(predicates)) != len(predicates):
        raise DeferConstructor()


def construct_last(context):
    constructed = context['constructed']
    skipped = context['skipped']
    dependencies = context['dependencies']
    if len(constructed) + len(skipped) < len(dependencies) - 1:
        raise DeferConstructor()


def construct_skip_no_value(value):
    if value is NULL:
        raise SkipConstructor()


class Spec(object):

    __slots__ = ('value', 'nodes', 'top', 'loc')

    @property
    def predicates(self):
        nodes = self.nodes
        if b'.' not in nodes:
            return NULL
        return nodes[b'.']

    @predicates.setter
    def predicates(self, val):
        nodes = self.nodes
        if not nodes:
            nodes = {}
            self.nodes = nodes
        nodes[b'.'] = val

    @property
    def template(self):
        nodes = self.nodes
        if b'?' not in nodes:
            return NULL
        return nodes[b'?']

    @template.setter
    def template(self, val):
        nodes = self.nodes
        if not nodes:
            nodes = {}
            self.nodes = nodes
        nodes[b'?'] = val

    @property
    def domain(self):
        top = self.top
        return top.top if self.loc else top

    @property
    def topspec(self):
        return self.top if self.loc else self

    @property
    def schemata(self):
        loc = self.loc
        topspec = self.top if loc else self
        domain = topspec.top
        domain_nodes = domain.nodes
        if b'$' not in domain_nodes:
            if domain_nodes is ():
                domain_nodes = {}
                domain.nodes = domain_nodes
            domain_nodes[b'$'] = Spec(top=domain, loc=(b'$',))
        return domain_nodes[b'$']

    @schemata.setter
    def schemata(self, spec):
        loc = self.loc
        topspec = self.top if loc else self
        domain = topspec.top
        domain_nodes = domain.nodes
        if spec.__class__ is not Spec:
            raise Error(what='invalid', message="schemata must be a Spec")
        if b'$' in domain_nodes:
            raise Error(what='already', message="schemata already set")
        if domain_nodes is ():
            domain_nodes = {}
            domain.nodes = domain_nodes
        spec.loc = (b'$',)
        spec.top = domain
        domain_nodes[b'$'] = spec

    def get_schema(self, key):
        key = key.rstrip(b'/')
        schemata_nodes = self.schemata.nodes
        if not schemata_nodes or key not in schemata_nodes:
            return NULL
        schema = schemata_nodes[key]
        return schema

    @property
    def constructions(self):
        loc = self.loc
        topspec = self.top if loc else self
        domain = topspec.top
        domain_nodes = domain.nodes
        if b'#' not in domain_nodes:
            if domain_nodes is ():
                domain_nodes = {}
                domain.nodes = domain_nodes
            domain_nodes[b'#'] = {}
        return domain_nodes[b'#']

    @constructions.setter
    def constructions(self, val):
        loc = self.loc
        topspec = self.top if loc else self
        domain = topspec.top
        domain_nodes = domain.nodes
        if val.__class__ is Spec:
            raise Error(what='invalid', message="constructions cannot be Spec")
        if b'#' in domain_nodes:
            raise Error(what='already', message="constructions already set")
        if domain_nodes is ():
            domain_nodes = {}
            domain.nodes = domain_nodes
        domain_nodes[b'#'] = val

    def to_source(self):
        if self is ANY:
            return ()

        source = {}
        nodes = self.nodes
        for k in nodes:
            v = nodes[k]
            if v.__class__ is Spec:
                v = v.to_source()
            else:
                v = {'=': v}
            source[k] = v
        if self.value is not ANY:
            source['='] = self.value
        if not source:
            source = ()
        return source

    @staticmethod
    def from_source(source):
        spec = Spec()
        spec.compile(source)
        return spec

    def compile_spec(self, source, register=False, complete=False):
        loc = self.loc
        topspec = self.top if loc else self
        spec = Spec(top=topspec.top, loc=())
        unknown_predicates = spec.compile(source, register=register)
        if complete and unknown_predicates:
            raise Error(what='unknown-predicates', data=unknown_predicates)
        return spec

    def compile_schemata(self, keys_and_sources):
        errs = []
        unknown_schemata = set()
        compile_schema = self.compile_schema
        for predicate_key, source in keys_and_sources:
            unknown = compile_schema(predicate_key, source, errs=errs)
            unknown_schemata.update(unknown)
        if errs:
            raise Error(what='compile-failed', errs=errs)
        return unknown_schemata

    def compile_schema(self, predicate, source, errs=None):
        if errs is None:
            errs = []
            raise_errs = True
        else:
            raise_errs = False

        schemata_nodes = self.schemata.nodes
        segments = predicate.split(b'.')
        subkey = segments[0]
        for segment in segments[1:-1]:
            subkey += b'.' + segment
            if subkey not in schemata_nodes:
                m = ("parent {parent!r} of predicate {predicate!r} "
                     "has not been registered")
                m = m.format(parent=subkey, predicate=predicate)
                e = Error(what='parent-predicate-not-found', message=m)
                collect_error(errs, e)

        schema_source = {
            '$/' + predicate: source,
        }
        unknown_schemata = self.compile(schema_source, errs=errs, register=True)
        if errs and raise_errs:
            raise Error(what='compile-failed', errs=errs)
        return unknown_schemata

    def compile(spec, doc, errs=None, register=False):

        loc = spec.loc
        topspec = spec.top if loc else spec

        if errs is None:
            raise_errs = True
            errs = []
        else:
            raise_errs = False

        source = normalize_source(doc)

        register_schemata = set()

        if b'$' in source:
            if not register:
                m = ("compile with register=True "
                     "to allow schemata config at global path '$'")
                raise Error(what='schemata-config-not-allowed',
                            loc=loc, message=m)

            schemata_source = source[b'$']
            del source[b'$']
            spec.schemata.config(schemata_source, errs=errs, strict=False)

        if b'#' in source:
            if not register:
                m = ("compile with register=True "
                     "to allow constructions config at global path '#'")
                raise Error(what='constructions-config-not-allowed',
                            loc=loc, message=m)

            constructions_source = source[b'#']
            del source[b'#']
            constructions = spec.constructions
            constructions.config(constructions_source, errs=errs, strict=False)

        if b'.' in source:
            source_predicates = source[b'.']
            del source[b'.']
            predicates_spec = Spec(top=topspec, loc=loc + (b'.',))
            predicates_spec.compile(source_predicates, errs, register)
            new_schemata = spec.config_deps(predicates_spec, errs, strict=False)
            register_schemata.update(new_schemata)

            if b'.' in spec.nodes:
                spec.nodes[b'.'].config(predicates_spec, errs=errs, strict=False)
            elif not spec.nodes:
                spec.nodes = {b'.': predicates_spec}
            else:
                spec.nodes[b'.'] = predicates_spec

        if b'=' in source:
            source_value = source[b'=']
            del source[b'=']
            spec.value = source_value

        if b'?' in source:
            source_template = source[b'?']
            del source[b'?']
            subloc = loc + (b'?',)
            # do not register schemata in templates
            template = Spec(top=topspec, loc=loc + (b'?',))
            template.compile(source_template, errs, False)
            if spec.nodes:
                spec.nodes[b'?'] = template
            else:
                spec.nodes = {b'?': template}

        nodes = spec.nodes
        if nodes is ():
            nodes = {}

        for key in sorted(source):
            val = source[key]
            if not val:
                # assert type(val) is Source  # because of normalize_source()
                if key in nodes:
                    continue

                nodes[key] = ANY
                continue

            source_spec = Spec(top=topspec, loc=loc + (key,))
            register_schemata.update(source_spec.compile(val, errs, register))

            if key in nodes:
                node_spec = nodes[key]
                if node_spec is ANY:
                    nodes[key] = source_spec.value \
                            if source_spec.nodes is () \
                            else source_spec
                else:
                    if node_spec.__class__ is not Spec:
                        node_spec = Spec(top=topspec,
                                         loc=loc + (key,),
                                         value=node_spec)
                    assert node_spec.loc == source_spec.loc
                    node_spec.config(source_spec, errs=errs)
                    if not errs and not node_spec.nodes:
                        nodes[key] = node_spec.value
            else:
                nodes[key] = source_spec \
                        if source_spec.nodes \
                        else source_spec.value

        if nodes:
            spec.nodes = nodes

        if errs and raise_errs:
            m = "compile failed"
            raise Error(what='compile-failed', errs=errs, loc=loc, message=m)

        return register_schemata

    def iterall(spec, what=b'=?./', preorder=False, postorder=True, path=()):

        iter_predicates = b'.' in what
        iter_values = b'=' in what
        iter_template = b'?' in what
        iter_spec = b'/' in what

        if spec is ANY:
            for t in preorder, postorder:
                if not t:
                    continue
                if iter_values or iter_spec:
                    yield path, ANY
            return

        value = spec.value
        if preorder:
            if iter_values:
                yield path, value
            if iter_spec:
                yield path, spec

        if iter_predicates and b'.' in spec.nodes:
            for t in spec.nodes[b'.'].iterall(
                what=what, preorder=preorder, postorder=postorder,
                path=path + (b'.',)
            ):
                yield t

        nodes = spec.nodes
        if nodes:
            for k, v in sorted(nodes.items()):
                if k in (b'?', b'.', b'#', b'$'):
                    continue
                if v is not ANY and v.__class__ is Spec:
                    for t in v.iterall(
                        what=what, preorder=preorder, postorder=postorder,
                        path=path + (k,)
                    ):
                        yield t
                else:
                    yield path + (k,), v

        if iter_template and b'?' in nodes:
            for t in nodes[b'?'].iterall(
                what=what, preorder=preorder, postorder=postorder,
                path=path + (b'?',)
            ):
                yield t

        if postorder:
            if iter_values:
                yield path, value
            if iter_spec:
                yield path, spec

    def config_deps(spec, predicates_spec, errs, mutable=True, strict=False):
        schemata_nodes = spec.schemata.nodes
        register_schemata = []
        for predicate_path, _ in predicates_spec.iterall(
            what=b'=', preorder=True, postorder=False
        ):
            if not predicate_path:
                continue

            predicate_key = b'.' + b'.'.join(predicate_path)
            if predicate_key in schemata_nodes:
                spec.config(schemata_nodes[predicate_key],
                            errs=errs, mutable=mutable, strict=strict)
            else:
                register_schemata.append(predicate_key)

        return register_schemata

    def config_nodes(spec, source_nodes, errs, mutable, strict):
        loc = spec.loc
        topspec = spec.top if loc else spec
        target_nodes = spec.nodes
        target_template = target_nodes[b'?'] if b'?' in target_nodes else NULL
        if not target_nodes:
            target_nodes = {}

        for key in sorted(source_nodes):

            subloc = loc + (key,)

            if key not in target_nodes:
                if not mutable:
                    e = Error(what='immutable-key', loc=subloc)
                    collect_error(errs, e)
                    continue

                if (target_template is NULL and not strict) or not target_nodes:
                    target = Spec(top=topspec, loc=subloc)
                elif (
                    target_template is NULL
                    or target_template.__class__ is not Spec
                    or target_template.value is not ANY
                ):
                    e = Error(what='no-template', loc=subloc)
                    collect_error(errs, e)
                    continue
                else:
                    target = target_template.clone(top=topspec, loc=subloc,
                                                   errs=errs, deps=True)
                if mutable:
                    target_nodes[key] = target

            else:
                target = target_nodes[key]
                if target is ANY:
                    target = Spec(top=topspec, loc=subloc)
                    if mutable:
                        target_nodes[key] = target
                elif target.__class__ is not Spec:
                    target = Spec(top=topspec, loc=subloc, value=target)
                    if mutable:
                        target_nodes[key] = target

            source = source_nodes[key]
            if source.__class__ is not Spec:
                target.config_value(source, errs, mutable)
            elif source is not ANY:
                target.config(source, errs=errs, mutable=mutable, strict=strict)
            else:
                # ignore if source is ANY
                pass

            target_val = target_nodes[key]
            if (
                target_val.__class__ is Spec
                and target_val is not ANY
                and target_val.nodes is ()
                and mutable
            ):
                target_nodes[key] = target_val.value

        if mutable and target_nodes:
            spec.nodes = target_nodes

    def config(spec, source, errs=None, mutable=True, strict=False):

        loc = spec.loc
        top = spec.top

        if errs is None:
            errs = []
            raise_errs = True
        else:
            raise_errs = False

        if source.__class__ is Spec:
            source_spec = source
        else:
            source_spec = Spec(top=top, loc=loc)
            source_spec.compile(source, errs=errs)

        mutable = mutable and spec.value is ANY

        source_nodes = source_spec.nodes
        if source_nodes:
            spec.config_nodes(source_nodes, errs, mutable, strict)

        source_value = source_spec.value
        if source_value is not ANY:
            spec.config_value(source_value, errs, mutable)

        if errs and raise_errs:
            raise Error(what='config-failed', errs=errs)

        return errs

    def clone(spec, loc=None, top=None, errs=None, deps=False):
        if errs is None:
            errs = []
            raise_errs = True
        else:
            raise_errs = False

        if loc is None:
            loc = ()
            if top is None:
                top = spec.domain

        newspec = Spec(top=top, loc=loc, value=spec.value)
        if spec is ANY:
            return newspec

        top = newspec.top
        loc = newspec.loc
        topspec = top if loc else newspec

        newspec.value = spec.value
        nodes = spec.nodes
        if nodes:
            newspec.nodes = {
                k: v.clone(top=topspec, loc=loc + (k,), deps=deps)
                if v.__class__ is Spec
                else Spec(top=top, loc=loc + (k,), value=v)
                for k, v in nodes.iteritems()
            }
            if deps and b'.' in newspec.nodes:
                predicates_spec = newspec.nodes[b'.']
                rp = newspec.config_deps(predicates_spec, errs,
                                         mutable=True, strict=False)
                if rp:
                    m = (
                        "if cloning a new node from a template, "
                        "all template predicates must be present "
                        "in order to be config()'ed into the new node."
                    )
                    e = Error(what='template-predicates-unknown',
                              message=m, loc=loc, data=rp)
                    collect_error(errs, e)
        else:
            newspec.nodes = ()

        if errs and raise_errs:
            raise Error(what='clone-failed', errs=errs)

        return newspec

    def config_value(spec, source_value, errs, mutable):
        target_value = spec.value
        if source_value is ANY:
            return
        elif target_value is ANY:
            if mutable:
                spec.value = source_value
            else:
                e = Error(what='immutable-value',
                          data=(target_value, source_value), loc=spec.loc)
                collect_error(errs, e)
        elif target_value == source_value:
            return
        else:
            e = Error(what='value-mismatch',
                      loc=spec.loc, data=(target_value, source_value))
            collect_error(errs, e)

    def getkwargs(spec):
        return {'__'.join(p): v for p, v in spec.iterall(what='=') if p}

    def iter_level_values(spec):
        nodes = spec.nodes
        for segment in nodes:
            if segment in (b'?', b'.', b'#', b'$'):
                continue
            val = nodes[segment]
            if val is not ANY and val.__class__ is Spec:
                val = val.value
            yield segment, val

    def iter_level_outputs(spec, artifacts):
        loc = spec.loc
        for key, _ in spec.iter_level_values():
            subloc = loc + (key,)
            val = artifacts[subloc] if subloc in artifacts else NULL
            yield subloc, val

    def extract_settings(spec, settings=None):
        all_settings = dict(settings) if settings is not None else {}
        nodes = spec.nodes
        if not nodes:
            return {}

        subspecs = []
        node_settings = {}

        for key, val in sorted(nodes.items()):
            if key in (b'?', b'.', b'$', b'#'):
                continue
            if key[:1] == b':':
                if val is ANY:
                    if key in all_settings:
                        node_settings[key] = all_settings[key]
                    else:
                        all_settings[key] = ANY
                        node_settings[key] = ANY
                elif val.__class__ is Spec:
                    val = val.value
                    if val is not ANY:
                        all_settings[key] = val
                        node_settings[key] = val
                    elif key in all_settings:
                        node_settings[key] = all_settings[key]
                    else:
                        all_settings[key] = ANY
                        node_settings[key] = ANY
                else:
                    all_settings[key] = val
                    node_settings[key] = val
            elif val.__class__ is Spec:
                subspecs.append((key, val))

        for key, subspec in subspecs:
            sub_settings = subspec.extract_settings(all_settings)
            if sub_settings:
                node_settings[key] = sub_settings

        return node_settings

    def construct(spec, constructibles=None, artifacts=None,
                  settings=None, constructions=None, errs=None):

        if artifacts is None:
            artifacts = {}

        if constructions is None:
            constructions = spec.constructions

        if constructibles is None:
            constructibles = constructions.keys()

        if settings is None:
            settings = spec.extract_settings()

        if errs is None:
            raise_errs = True
            errs = []
        else:
            raise_errs = False

        loc = spec.loc
        topspec = spec.top if loc else spec

        nodes = spec.nodes

        if b'.' in nodes:
            nodes[b'.'].construct(
                constructibles=constructibles,
                settings=settings,
                artifacts=artifacts,
                constructions=constructions,
                errs=errs,
            )

        # do not construct templates.
        # if tempted to use a template to construct a generic artifact
        # then create use config() to create a 'default' non-template entry
        # that will be initialized to the template and will be constructed.

        if nodes is not ():
            for key, subspec in sorted(spec.nodes.items()):
                if key in (b'?', b'.', b'$', b'#'):
                    continue

                if subspec is ANY:
                    continue

                if subspec.__class__ is not Spec:
                    value = subspec
                    subspec = Spec(top=topspec, loc=loc + (key,))
                    subspec.value = value

                subsettings = (
                    settings[key]
                    if key[:1] != b':' and key in settings
                    else {}
                )

                subspec.construct(
                    constructibles=constructibles,
                    artifacts=artifacts,
                    settings=subsettings,
                    constructions=constructions,
                    errs=errs,
                )

        if not errs:
            for construction in constructibles:
                spec.call_constructors(
                    construction=construction,
                    artifacts=artifacts,
                    settings=settings,
                    constructions=constructions,
                    errs=errs,
                )

        if errs and raise_errs:
            raise Error(what='construction-failed', loc=spec.loc, errs=errs,
                        message='construction failed')

        return artifacts


    def call_constructors(spec, construction, artifacts, settings,
                          constructions, errs):

        if b'.' not in spec.nodes:
            return []

        spec_predicates = spec.nodes[b'.']

        constructors = constructions[construction]

        if not settings:
            settings = {}

        working_predicates = [
            b'.' + b'.'.join(k) for k, _ in
            spec_predicates.iterall(what='=',  preorder=False, postorder=True)
            if k
        ]

        if construction not in artifacts:
            artifacts[construction] = {}

        construction_artifacts = artifacts[construction]

        output = (
            construction_artifacts[spec.loc]
            if spec.loc in construction_artifacts
            else NULL
        )

        value = spec.value
        if value is ANY:
            value = NULL

        context = {
            'spec': spec,
            'loc': spec.loc,
            'top_spec': spec.top if spec.loc else spec,
            'constructions': constructions,
            'construction': construction,
            'constructors': constructors,
            'value': value,
            'output': output,
            'artifacts': construction_artifacts,
            'global_artifacts': artifacts,
            'settings': settings,
            'dependencies': working_predicates,
            'schemata': spec.schemata,
            'constructed': set(),
            'skipped': set(),
            'round': 0,
            'errs': errs,
            'context': None,
        }

        old_deferred_predicates = None
        while True:
            deferred_predicates = []
            for predicate in working_predicates:
                if predicate not in constructors:
                    context['skipped'].add(predicate)
                    # m = ("cannot find constructor {predicate!r} "
                    #      "in construction {construction!r}")
                    # m = m.format(predicate=predicate, construction=construction)
                    # e = Error(what='not-found', loc=spec.loc,
                    #           data=predicate, message=m)
                    # collect_error(errs, e)
                    continue
                else:
                    constructor = constructors[predicate]

                context['predicate'] = predicate
                args = spec.getpath(predicate)
                args = args.getkwargs() if args.__class__ is Spec else {}
                context['args'] = args

                try:
                    output = constructor(context=context)
                    context['constructed'].add(predicate)
                    construction_artifacts[spec.loc] = output
                    context['output'] = output
                except SkipConstructor:
                    context['skipped'].add(predicate)
                except DeferConstructor:
                    deferred_predicates.append(predicate)
                except Error as e:
                    collect_error(errs, e)
                    continue

            if not deferred_predicates:
                break

            if deferred_predicates == old_deferred_predicates:
                m = "{loc!r}/{predicate!r}: constructor deadlock {deferred!r}"
                m = m.format(loc=spec.loc, predicate=predicate,
                             deferred=deferred_predicates)
                raise TypeError(m)

            old_deferred_predicates = deferred_predicates
            working_predicates = deferred_predicates
            context['round'] += 1

        if context['skipped']:
            skipped_key = construction + '#skipped'
            if skipped_key not in artifacts:
                artifacts[skipped_key] = {}

            skipped = artifacts[skipped_key]
            skipped[spec.loc] = context['skipped']

    def __repr__(self):
        return pformat(self.to_source())

    def iteritems(self, keys=False):
        it = self.iterall(what='=.?', preorder=True, postorder=False)
        return ((path_to_key(k), v) for k, v in it) if keys else it

    def items(self):
        return list(self.iteritems())

    def iterkeys(self):
        return (k for k, v in self.iteritems())

    def keys(self):
        return list(self.iterkeys())

    def itervalues(self):
        return (v for k, v in self.iteritems())

    def values(self):
        return list(self.itervalues())

    def getpath(self, key):
        path = key_to_path(key) if isinstance(key, basestring) else key
        return getpath(self, path)

    def setval(self, key, val):
        path = key_to_path(key) if isinstance(key, basestring) else key
        return setval(self, path, val)

    def __getitem__(self, key):
        path = key_to_path(key) if isinstance(key, basestring) else key
        return getval(self, path)

    def __setitem__(self, key, val):
        path = key_to_path(key) if isinstance(key, basestring) else key
        return setval(self, path, val)

    def __contains__(self, key):
        path = key_to_path(key) if isinstance(key, basestring) else key
        val = getval(self, path)
        return val is not NULL

    def __iter__(self):
        return self.iterkeys()

    def __len__(self):
        return len(self.nodes)

    def __nonzero__(self):
        r = (
            self.nodes or
            self.value is not ANY
        )
        return True if r else False

    def __eq__(self, other):
        if not other.__class__ is Spec:
            return False

        return all(
            a == b
            for a, b in izip(self.iteritems(), other.iteritems())
        )


ANY = Spec()
ANY.nodes = ()
ANY.value = ANY
ANY.loc = ()
ANY.top = ANY


def getval(self, path=(), default=ANY, missing=NULL):
    spec = getpath(self, path=path)
    if spec is NULL:
        return missing
    elif spec is ANY:
        return default
    elif spec.__class__ is not Spec:
        return spec
    else:
        value = spec.value
        return default if value is ANY else value


Spec.getval = getval


def spec_init(self, top=None, loc=(), value=NULL, nodes=(),
              schemata=None, constructions=None):
    if top is None:
        if loc:
            m = "cannot put a topspec at a nonempty path {loc!r}"
            m = m.format(loc=loc)
            raise TypeError(m)
        top = self
    elif loc:
        if top.__class__ is not Spec:
            m = "topspec must be a Spec at nonempty path {loc!r}"
            m = m.format(loc=loc)
            raise TypeError(m)
    elif top.__class__ is not Spec:
        m = "topspec must be a Spec at the root (empty path), not {0!r}"
        m = m.format(top)
        raise TypeError(m)

    self.top = top
    self.loc = loc
    self.value = ANY if value is NULL else value
    self.nodes = nodes
    if schemata is not None:
        self.schemata = schemata
    if constructions is not None:
        self.constructions = constructions


Spec.__init__ = spec_init


MAXINT = sys.maxint
MININT = -sys.maxint - 1


number_sources = [
    (
        '.number',
        {
            '.number': (),
        },
    ),
]


documentation_sources = [
    (
        '.documentation',
        {
            '.documentation': (),
        },
    ),
]


integer_sources = [
    (
        '.integer',
        {
            '.integer': (),
        },
    ),
    (
        '.integer.min',
        {
            '.integer.min': {
                '.number': None,
                '.documentation': 'minimum permitted value',
            },
        },
    ),
    (
        '.integer.max',
        {
            '.integer.max': {
                '.number': None,
                '.documentation': 'maximum permitted value',
            },
        },
    ),
    (
        '.integer.randomize',
        {
            '.integer.randomize': {
                '.bool': None,
                '.documentation': (
                    'create a random conforming value '
                    'if no value exists at construction time'
                ),
            },
        },
    ),
]


@make_constructor
def construct_integer(spec, value, args, loc):
    min = args['min'] if 'min' in args else None
    max = args['max'] if 'max' in args else None
    randomize = args['randomize'] if 'randomize' in args else False

    if value is NULL:
        if randomize:
            _min = MININT if min is None else min
            _max = MAXINT if max is None else max
            output = randint(_min, _max)
        else:
            raise SkipConstructor()

    elif isinstance(value, basestring):
        if not value.isdigit():
            m = "data given not made of integer digits"
            raise Error(what='invalid', loc=loc, data=value, message=m)

        output = int(value)

    elif not isinstance(value, (int, long)):
        m = "cannot make out an integer out of data given"
        raise Error(what='invalid', loc=loc, data=value, message=m)

    else:
        output = value

    if min is not None and output < min:
        m = "integer {output!r} less than min {min!r}"
        m = m.format(output=output, min=min)
        raise Error(what='invalid', loc=loc, data=(output, min), message=m)

    if max is not None and output > max:
        m = "integer {output!r} greater than max {max!r}"
        m = m.format(output=output, max=max)
        raise Error(what='invalid', loc=loc, data=(output, max), message=m)

    return output


bytes_sources = [
    (
        '.bytes',
        {
            '.bytes': (),
        },
    ),
]


@make_constructor
def construct_bytes(value):
    construct_skip_no_value(value)
    return str(value)


bool_sources = [
    (
        '.bool',
        {
            '.bool': (),
        },
    ),
]


@make_constructor
def construct_bool(value):
    construct_skip_no_value(value)
    return bool(value)


text_sources = [
    (
        '.text',
        {
            '.text': (),
            '.bytes': (),
        },
    ),
    (
        '.text.minlen',
        {
            '.text.minlen': {
                '.integer': {
                    'min': 0,
                },
                '.documentation': 'minimum permitted character length',
            },
        },
    ),
    (
        '.text.maxlen',
        {
            '.text.maxlen': {
                '.integer': {
                    'min': 0,
                },
                '.documentation': 'maximum permitted character length',
            },
        },
    ),
    (
        '.text.regex',
        {
            '.text.regex': {
                '.bytes': (),
                '.documentation': (
                    'a regular expression to be matched against the value'
                ),
            },
        },
    ),
    (
        '.text.alphabet',
        {
            '.text.alphabet': {
                '.bytes': (),
            },
        },
    ),
    (
        '.text.encoding',
        {
            '.text.encoding': {
                '.bytes': (),
                '.documentation': 'if given, use it to decode bytes to unicode',
            },
        },
    ),
    (
        '.text.excluded',
        {
            '.text.excluded': {
                '.bytes': (),
                '.documentation': 'a string of individually allowed characters',
            },
        },
    ),
    (
        '.text.randomize',
        {
            '.text.randomize': {
                '.bool': (),
                '.documentation': (
                    'create a random conforming value '
                    'if instance provides no value'
                ),
            },
        },
    ),
]


_text_default_alphabet = b''.join(chr(x) for x in xrange(256))


@make_constructor
def construct_text(spec, predicate, args, value, loc):
    text = value
    regex = args['regex'] if 'regex' in args else None
    encoding = args['encoding'] if 'encoding' in args else ''
    minlen = args['minlen'] if 'minlen' in args else None
    maxlen = int(args['maxlen']) if 'maxlen' in args else None
    alphabet = args['alphabet'] if 'alphabet' in args else None
    excluded = args['excluded'] if 'excluded' in args else ''
    randomize = args['randomize'] if 'randomize' in args else False

    if text is NULL:
        if randomize:
            if alphabet is None:
                alphabet = _text_default_alphabet

            if regex is not None:
                m = "{loc!r}: cannot randomize when 'regex' is given"
                m = m.format(loc=loc)
                raise Error(what='unsupported', message=m)

            if excluded:
                alphabet = ''.join(set(alphabet) - set(excluded))

            text = ''.join(choice(alphabet)
                           for _ in xrange(randint(minlen, maxlen)))
        else:
            raise SkipConstructor()

    if isinstance(text, str):
        if encoding:
            text = text.decode(encoding)

    elif not isinstance(text, unicode):
        m = "text data is neither str nor unicode"
        m = m.format(loc=loc, data=text, message=m)
        raise Error(what='invalid', message=m, loc=loc, data=text)

    if regex is not None:
        pattern = re.compile(regex, re.UNICODE)
        if pattern.match(text) is None:
            m = "text data does not match regex {regex!r}"
            m = m.format(regex=regex)
            raise Error(what='invalid', loc=loc, data=text, message=m)

    text_len = len(text)
    if text_len < minlen:
        m = "text data length {len!r} less than minlen {minlen!r}"
        m = m.format(len=len, minlen=minlen)
        raise Error(what='invalid', loc=loc, data=text, message=m)

    if maxlen is not None and text_len > maxlen:
        m = "text data length {len!r} greater than maxlen {maxlen!r}"
        m = m.format(len=len, maxlen=maxlen)
        raise Error(what='invalid', loc=loc, data=text, message=m)

    if alphabet is not None:
        alphabet = ''.join(set(alphabet) - set(excluded))
        for c in text:
            if c not in alphabet:
                m = "char {c!r} in text data is not in alphabet {alphabet!r}"
                m = m.format(c=c, alphabet=alphabet)
                raise Error(what='invalid', loc=loc, data=text, message=m)

    elif excluded:
        for c in excluded:
            if c in text:
                m = "forbidden char {c!r} found in text data"
                m = m.format(c=c)
                raise Error(what='invalid', loc=loc, data=text, message=m)

    return text


object_sources = [
    (
        '.object',
        {
            '.object': {},
            'class': {
                '.bytes': (),
            },
            'args': (),
        },
    ),
]


@make_constructor
def construct_object(predicate, spec, value, loc):

    classpath = spec['class']
    modulepath, sep, classname = classpath.partition(':')
    try:
        module = importlib.import_module(modulepath)
    except ImportError as e:
        m = "Error loading module {modulepath!r}: {msg!r}"
        m = m.format(modulepath=modulepath, msg=str(e))
        raise Error(what='invalid', loc=loc, data=classpath, message=m)

    classtype = getattr(module, classname, None)
    if classtype is None:
        m = "Cannot find {classname!r} in module {modulepath!r}"
        m = m.format(classname=classname, modulepath=modulepath)
        raise Error(what='invalid', loc=loc, data=classpath, message=m)

    if value is NULL:
        kwargs = spec.getpath('args').getkwargs()
        try:
            value = classtype(**kwargs)
        except Exception as e:
            m = "Error constructing {classpath!r}: {msg!r}"
            m = m.format(classpath=classpath, msg=str(e))
            raise Error(what='invalid', loc=loc,
                        data=(classpath, kwargs), message=m)
    elif not isinstance(value, classtype):
        m = ("Existing object {obtype!r} "
             "is not an instance of {classpath!r}")
        m = m.format(obtype=type(value), classpath=classpath)
        raise Error(what='invalid', loc=loc, data=value, message=m)

    return value


base_schemata_sources = (
    bool_sources +
    bytes_sources +
    number_sources +
    documentation_sources +
    integer_sources +
    text_sources +
    object_sources
)


global_domain = Spec()
global_domain.compile({'$/?': ANY}, register=True)
global_domain.compile_schemata(base_schemata_sources)

base_constructions = {
    'base': {
        '.bool': construct_bool,
        '.bytes': construct_bytes,
        '.integer': construct_integer,
        '.text': construct_text,
        '.object': construct_object,
    },
}

global_domain.constructions = base_constructions


class Processor(object):

    def process(self, data):
        pass

    def cleanup(self, name, exc, data):
        return {}

    def __init__(self, name, reads=(), writes=(),
                 process=None, cleanup=None):

        for key in chain((name,), reads, writes):
            if key.__class__ is not Bytes:
                m = "{0!r}: not a string of bytes".format(key)
                raise Error(what='invalid', message=m)

        self.name = name
        self.reads = frozenset(reads)
        self.writes = frozenset(writes)

        if process is not None:
            if not callable(process):
                m = "{0!r}: process argument not a callable".format(process)
                raise Error(what='invalid', message=m)
            self.process = process

        if cleanup is not None:
            if not callable(cleanup):
                m = "{0!r}: cleanup argument not a callable".format(cleanup)
                raise Error(what='invalid', message=m)
            self.cleanup = cleanup

    @classmethod
    def make(cls, name=None, reads=(), writes=()):
        def make_processor(fn, name=name, reads=reads, writes=writes):
            if isinstance(fn, FunctionType):
                if name is None:
                    name = fn.func_name
            elif callable(fn):
                if name is None:
                    name = fn.__class__.__name__
            else:
                m = "{0!r}: not a FunctionType or callable".format(fn)
                raise Error(what='invalid', message=m)

            return Processor(name=name, reads=reads, writes=writes, process=fn)

        return make_processor


class Runtime(Mapping):

    def __init__(self, spec):
        if not isinstance(spec, Spec):
            m = "spec is not Spec, but {0}".format(type(spec))
            raise TypeError(m)

        self.spec = spec

        self.processors = {}
        self.reader_index = defaultdict(list)
        self.writer_index = defaultdict(list)
        self.pending = None
        self.waiting = None

        self.namespace = None
        self.initial_namespace = {
            path_to_key(path): value
            for path, value
            in spec.iterall(what='=', preorder=True, postorder=False)
        }
        self.reset()

    def __iter__(self):
        return iter(self.namespace)

    def __contains__(self, key):
        return key in self.namespace

    def __len__(self):
        return self.namespace.__len__()

    def __getitem__(self, key):
        return self.namespace[key] if key in self.namespace else NULL

    def __setitem__(self, key, val):
        ns = self.namespace
        if key not in ns:
            m = "{key!r}: key not in namespace".format(key=key)
            raise Error(what='not-found', message=m)

        ns[key] = val

    def write(self, key, value, writer=None):
        self[key] = value
        self.register_write(key, writer)

    def register_write(self, key, writer=None):
        writer_index = self.writer_index
        if key in writer_index:
            writers = writer_index[key]
            writers.discard(writer)
            if not writers:
                del writer_index[key]
        else:
            writers = ()

        reader_index = self.reader_index
        if key not in reader_index:
            return

        readers = reader_index[key]
        pending = self.pending
        waiting = self.waiting

        for reader in list(readers):
            if reader not in pending:
                continue

            if writers and reader not in writers:
                continue

            deps = pending[reader]
            deps.discard(key)
            if not deps:
                del pending[reader]
                waiting.append(reader)
                readers.discard(reader)

        if not readers:
            del reader_index[key]

    def get_input_keys(self):
        writer_index = self.writer_index
        input_keys = []
        for name, deps in self.pending.items():
            for read_key in deps:
                if read_key not in writer_index:
                    input_keys.append(read_key)
        return input_keys

    def reset_processors(self):
        reader_index = {}
        writer_index = {}
        waiting = []
        pending = {}

        for name, proc in self.processors.items():
            pending_set = set(proc.reads)
            if pending_set:
                pending[name] = pending_set
            else:
                waiting.append(name)

            for read_key in proc.reads:
                if read_key not in reader_index:
                    reader_index[read_key] = set()
                reader_index[read_key].add(name)

            for write_key in proc.writes:
                if write_key not in writer_index:
                    writer_index[write_key] = set()
                writer_index[write_key].add(name)

        self.reader_index = reader_index
        self.writer_index = writer_index
        self.pending = pending
        self.waiting = waiting
        self.processed = []

    def reset_data(self):
        self.namespace = dict(self.initial_namespace)

    def reset(self):
        self.reset_data()
        self.reset_processors()

    def iterkeys(self):
        return self.namespace.iterkeys()

    def itervalues(self):
        return self.namespace.itervalues()

    def keys(self):
        return self.namespace.keys()

    def values(self):
        return self.namespace.values()

    def iterlevel(self, key):
        path = key_to_path(key)
        subspec = getpath(self.spec, path)
        if subspec is NULL:
            m = "{0!r}: key not found".format(key)
            raise Error(what='not-found', message=m)

        elif subspec is ANY:
            return

        elif subspec.__class__ is not Spec:
            yield '', subspec
            return

        namespace = self.namespace
        for segment, val in subspec.iter_level_values():
            subkey = path_to_key(path + (segment,))
            yield segment, namespace[subkey]

    def getlevel(self, key):
        return dict(self.iterlevel(key))

    def iterpath(self, key):
        path = key_to_path(key)
        subspec = getpath(self.spec, path)
        if subspec is NULL:
            m = "{0!r}: key not found".format(key)
            raise Error(what='not-found', message=m)

        elif subspec is ANY:
            return

        elif subspec.__class__ is not Spec:
            yield b'', subspec
            return

        namespace = self.namespace
        for subpath, val in subspec.iterall(
            what='=', preorder=True, postorder=False
        ):
            subkey = path_to_key(subpath)
            ns_key = path_to_key(path + subpath)
            yield subkey, namespace[ns_key]

    def getpath(self, key):
        return dict(self.iterpath(key))

    def insert(self, doc, path=(), writer=NULL):
        if path.__class__ is not tuple:
            path = key_to_path(path)
        for key, val in doc.items():
            if key == b'=':
                continue
            subpath = path + (key,)
            if val.__class__ is Data:
                val = val.value
            elif hasattr(val, 'get'):
                subdoc = val
                self.insert(subdoc, path=subpath, writer=writer)
                continue
            write_key = path_to_key(subpath)
            self[write_key] = val
            if writer is not NULL:
                self.register_write(write_key, writer)

        if b'=' in doc:
            write_key = path_to_key(path)
            self[write_key] = doc[b'=']
            if writer is not NULL:
                self.register_write(write_key, writer)

    def add_processor(self, processor):
        if not isinstance(processor, Processor):
            m = "{0!r} is not Processor".format(processor)
            raise Error(what='invalid', message=m)

        name = processor.name
        if name in self.processors:
            m = "{0}: processor already exists".format(name)
            raise Error(what='already', message=m)

        self.processors[name] = processor

        namespace = self.namespace

        reader_index = self.reader_index
        if processor.reads:
            self.pending[name] = set(processor.reads)
            for read_key in processor.reads:
                if read_key not in namespace:
                    m = "{0!r}: read key not in namespace".format(read_key)
                    raise Error(what='no-read-key', message=m, data=read_key)

                if read_key not in reader_index:
                    reader_index[read_key] = set()
                reader_index[read_key].add(name)
        else:
            self.waiting.append(name)

        writer_index = self.writer_index
        for write_key in processor.writes:
            if write_key not in namespace:
                m = "{0!r}: write key not in namespace".format(write_key)
                raise Error(what='no-write-key', message=m, data=write_key)

            if write_key not in writer_index:
                writer_index[write_key] = set()
            writer_index[write_key].add(name)


    def print_out_dot_graph(self, outfile):
        keys_seen = set()

        header = (
            'digraph {\n'
            '    node [fontname="Courier"];\n'
            '    edge [fontname="Courier"];\n'
            '\n'
        )
        outfile.write(header)

        for name, proc in sorted(self.processors.iteritems()):
            node = '    "{name}" [shape=oval]\n'
            node = node.format(name=proc.name)
            outfile.write(node)

            for read_key in proc.reads:
                if read_key not in keys_seen:
                    keys_seen.add(read_key)
                    node = '    "{key}" [shape=box]\n'
                    node = node.format(key=read_key)
                    outfile.write(node)

                edge = '    "{key}" -> "{name}"\n'
                edge = edge.format(key=read_key, name=proc.name)
                outfile.write(edge)

            for write_key in proc.writes:
                if write_key not in keys_seen:
                    keys_seen.add(write_key)
                    node = '    "{key}" [shape=box]\n'
                    node = node.format(key=write_key)
                    outfile.write(node)
                edge = '    "{name}" -> "{key}"\n'
                edge = edge.format(key=write_key, name=proc.name)
                outfile.write(edge)

        footer = (
            '}\n'
        )
        outfile.write(footer)

    def get_schedule(self):
        self.reset_processors()
        register_write = self.register_write
        input_keys = self.get_input_keys()
        for key in input_keys:
            register_write(key)
        results, pending, _ = self.process({}, dry=True)
        schedule = [k for k, v in results]
        self.reset_processors()
        return schedule, pending

    def process_one(self, processor, dry=False):
        data = {}
        for key in processor.reads:
            data[key] = self[key]

        name = processor.name
        data['$runtime'] = self
        self.processed.append(name)
        output = {} if dry else processor.process(data)

        register_write = self.register_write
        writes = processor.writes
        for key in writes:
            if key in output:
                self[key] = output[key]
                del output[key]
            register_write(key, name)
        return output

    def cleanup_one(self, processor, name, exc, dry=False):
        data = {}
        for key in processor.reads:
            data[key] = self[key]

        data['$runtime'] = self
        output = {} if dry else processor.cleanup(name, exc, data)

        register_write = self.register_write
        writes = processor.writes
        name = processor.name
        for key in writes:
            if key in output:
                self[key] = output[key]
        return output

    def process_all(self, initdata=None, docdata=None):
        r = self.process(initdata=initdata, docdata=docdata)
        results, pending, errs = r
        if errs:
            raise Error(what='process-error', errs=errs)

        if pending:
            raise Error(what='process-pending', data=pending)

        unknown_keys = [(name, output) for name, output in results if output]
        if unknown_keys:
            raise Error(what='process-unknown-keys', data=unknown_keys)
        schedule = [name for name, _ in results]
        return schedule

    def process(self, initdata=None, docdata=None, dry=False):
        errs = []
        processors = self.processors
        process_one = self.process_one
        register_write = self.register_write
        results = []
        name = None

        if initdata is not None:
            for key in initdata:
                val = initdata[key]
                self[key] = val
                register_write(key)

        if docdata is not None:
            self.insert(docdata, writer=None)

        try:
            while True:
                waiting = self.waiting
                if not waiting:
                    break

                self.waiting = []
                for name in waiting:
                    processor = processors[name]
                    result = process_one(processor, dry=dry)
                    results.append((name, result))
        except Exception as e:
            errs.append(e)
            for pname in reversed(self.processed):
                if pname not in processors:
                    continue

                proc = processors[pname]
                try:
                    self.cleanup_one(proc, name, e, dry=dry)
                except Exception as ee:
                    errs.append(ee)

        return results, self.pending, errs


def negotiate(spec, positions, our_signer=None, our_position=None):

    validation_errors = {}
    valid_positions = []
    compatibility_errors = {}
    compatible_positions = []
    signers = set()
    consensus = {}
    path_statuses = {}
    node_statuses = {}
    our_path_analysis = None
    our_node_analysis = None
    candidate_spec = spec.clone()

    for path, value in spec.iteritems(keys=True):
        if value is ANY:
            continue

        consensus[path] = {value: (None, set())}

    spec_positions = []
    for signer, signer_source in positions:
        signer_spec = (
            signer_source
            if signer_source.__class__ is Spec
            else Spec.from_source(signer_source)
        )
        spec_positions.append((signer, signer_spec))

    extract_positions(spec, spec_positions, consensus, candidate_spec,
                      signers, valid_positions, validation_errors,
                      compatible_positions, compatibility_errors)

    nr_signers = len(signers)

    analyze_positions(consensus, our_signer, nr_signers,
                      path_statuses, node_statuses)

    if our_position is not None:
        our_position_spec = (
            our_position
            if our_position.__class__ is Spec else
            Spec.from_source(our_position)
        )
        our_valid_positions = []
        our_validation_errors = {}
        our_compatible_positions = []
        our_compatibility_errors = {}
        extract_positions(spec, [(our_signer, our_position_spec)], consensus,
                          candidate_spec, signers,
                          our_valid_positions, our_validation_errors,
                          our_compatible_positions, our_compatibility_errors)

        if our_validation_errors:
            m = "our_position is invalid"
            raise Error(what='invalid', message=m)

        valid_positions.extend(our_valid_positions)

        if not our_compatibility_errors:
            compatible_positions.extend(our_compatible_positions)

        nr_signers = len(signers)

        our_path_statuses = {}
        our_node_statuses = {}

        analyze_positions(consensus, our_signer, nr_signers,
                          our_path_statuses, our_node_statuses)

        our_path_analysis = compare_path_statuses(path_statuses, our_path_statuses)
        our_node_analysis = compare_node_statuses(node_statuses, our_node_statuses)

    analysis = {
        'candidate_spec': candidate_spec,
        'signers': signers,
        'consensus': consensus,
        'validation_errors': validation_errors,
        'valid_positions': valid_positions,
        'compatibility_errors': compatibility_errors,
        'compatible_positions': compatible_positions,
        'path_statuses': path_statuses,
        'node_statuses': node_statuses,
        'our_path_analysis': our_path_analysis,
        'our_node_analysis': our_node_analysis,
    }

    return analysis


def extract_positions(spec, spec_positions, consensus, candidate_spec,
                      signers, valid_positions, validation_errors,
                      compatible_positions, compatibility_errors):

    for signer, signer_spec in spec_positions:
        signers.add(signer)
        error_paths = ()
        newspec = spec.clone()
        try:
            newspec.config(signer_spec)
        except Error as e:
            if e.what != 'config-failed':
                raise
            error_paths = {err.loc: err.what for err in e.errs}
        else:
            valid_positions.append((signer, signer_spec))

        for path, value in signer_spec.iteritems(keys=True):
            if path in error_paths:
                continue

            if path in consensus:
                path_consensus = consensus[path]
                if value in path_consensus: 
                    path_issuer, path_signers = path_consensus[value]
                    path_signers.add(signer)
                else:
                    path_consensus[value] = (signer, set())
            else:
                consensus[path] = {value: (signer, set())}

        if error_paths:
            validation_errors[signer] = error_paths

    for signer, signer_spec in valid_positions:
        error_paths = None
        try:
            candidate_spec.config(signer_spec)
        except Error as e:
            if e.what != 'config-failed':
                raise
            error_paths = {err.loc: err.what for err in e.errs}
        else:
            compatible_positions.append((signer, signer_spec))

        if error_paths:
            compatibility_errors[signer] = error_paths


def analyze_positions(consensus, our_signer, nr_signers,
                      path_statuses, node_statuses):

    consensus_items = sorted(consensus.iteritems())
    consensus_items.reverse()
    for path, path_consensus in consensus_items:
        if len(path_consensus) != 1:
            path_ack = 'CONFLICT'
            path_nr_pending = nr_signers
            path_issuer = None
            path_status = (path_nr_pending, path_issuer, path_ack)
        else:
            path_value, (path_issuer, path_signers) = path_consensus.items()[0]
            path_nr_pending = nr_signers - len(path_signers)
            ack = 'ACK' if our_signer in path_signers else 'NOACK'
            path_status = (path_nr_pending, path_issuer, ack)

        path_statuses[path] = path_status
        set_consensus_node_status(node_statuses, path, path_status)


def set_consensus_node_status(node_statuses, path, path_status):
    path_nr_pending, path_issuer, path_ack = path_status
    original_path = path
    while True:
        if path not in node_statuses:
            node_statuses[path] = path_nr_pending, path_ack
        else:
            node_nr_pending, node_ack = node_statuses[path]
            if path_nr_pending > node_nr_pending:
                node_nr_pending = path_nr_pending

            if node_ack != 'CONFLICT' and path_ack != node_ack:
                if path_ack == 'CONFLICT':
                    node_ack = path_ack
                elif path_ack == 'NOACK':
                    node_ack = path_ack

            node_statuses[path] = node_nr_pending, node_ack

        if not path:
            break

        path, sep, _ = path.rpartition('/')


def compare_path_statuses(path_statuses, our_path_statuses):
    our_path_analysis = {}
    path_statuses_keys = set(path_statuses)
    for path, path_status in our_path_statuses.iteritems():
        path_nr_pending, path_issuer, path_ack = path_status
        if path in path_statuses_keys:
            path_statuses_keys.discard(path)
            old_path_status = path_statuses[path]
        else:
            old_path_status = None, None, None
        our_path_analysis[path] = old_path_status, path_status

    for path in path_statuses_keys:
        old_path_status = path_statuses[path]
        our_path_analysis[path] = old_path_status

    return our_path_analysis


def compare_node_statuses(node_statuses, our_node_statuses):
    our_node_analysis = {}
    node_statuses_keys = set(node_statuses)
    for path, node_status in our_node_statuses.iteritems():
        if path in node_statuses_keys:
            node_statuses_keys.discard(path)
            old_node_status = node_statuses[path]
        else:
            old_node_status = None
        our_node_analysis[path] = old_node_status, node_status

    for path in node_statuses_keys:
        old_node_status = path_statuses[path]
        our_node_analysis[path] = old_node_status, None

    return our_node_analysis
