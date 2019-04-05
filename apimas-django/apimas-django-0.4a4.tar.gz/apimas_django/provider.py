import logging
from collections import defaultdict
from django.conf.urls import url
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from apimas import utils
from apimas.errors import InvalidSpec
from apimas_django.execution import ApimasAction
from apimas_django.wrapper import django_views
from apimas_django.predicates import domain
from apimas_django.collect_construction import collect_processors
import specular

logger = logging.getLogger('apimas')


def read_action_spec(action_spec):
    param_keys = ('method', 'status_code', 'content_type',
                  'on_collection', 'url',)
    params = {k:specular.getval(v, default=None)
              for k, v in action_spec.nodes.items()
              if k in param_keys}
    return params


@specular.make_constructor
def collection_django_constructor(context, loc):
    logger.info("Constructing collection %s", loc)
    views = defaultdict(dict)
    for value in specular.iter_spec_artifacts(context, ('fields',)):
        views.update(value)

    for view_spec in specular.iter_spec_artifacts(context, ('actions',)):
        urlpattern, method, view = view_spec
        views[urlpattern][method] = view
    return views


def named_pattern(name):
    return '(?P<%s>[^/.]+)' % name


def join_urls(*args):
    """
    Join arguments into a url.

    >>> join_urls("http://www.test.org", "path")
    'http://www.test.org/path'
    >>> join_urls("http://www.test.org/", "path")
    'http://www.test.org/path'
    >>> join_urls("http://www.test.org", "/path")
    'http://www.test.org/path'
    >>> join_urls("http://www.test.org/", "/path")
    'http://www.test.org/path'
    >>> join_urls("http://www.test.org/", "/path/")
    'http://www.test.org/path/'
    >>> join_urls("http://www.test.org/a/b", "c/d")
    'http://www.test.org/a/b/c/d'
    >>> join_urls("http://www.test.org/a/b/", "c/d")
    'http://www.test.org/a/b/c/d'
    >>> join_urls("http://www.test.org/a/b", "/c/d")
    'http://www.test.org/a/b/c/d'
    >>> join_urls("http://www.test.org/a/b/", "/c/d")
    'http://www.test.org/a/b/c/d'
    >>> join_urls("http://www.test.org/a/b/", "/c/d/", "/e/f/")
    'http://www.test.org/a/b/c/d/e/f/'
    >>> join_urls("/path1", "/path")
    '/path1/path'
    >>> join_urls("path1", "/path")
    'path1/path'
    >>> join_urls("path1/")
    'path1/'
    >>> join_urls("path1/", "path2", "path3")
    'path1/path2/path3'
    >>> join_urls("", "path2", "path3")
    'path2/path3'
    >>> join_urls("", "", "")
    ''
    """
    args = filter(bool, args)

    if len(args) == 0:
        return ''

    if len(args) == 1:
        return args[0]

    return "/".join([args[0].rstrip("/")] +
                    [a.strip("/") for a in args[1:-1]] +
                    [args[-1].lstrip("/")])


def _construct_url(path, action_url):
    unpacked_action_url = action_url.replace('*', named_pattern('pk'))
    url = join_urls(path, unpacked_action_url).rstrip('/') + '/'
    url_pattern = r'^' + url + '$'
    return url_pattern


def get_processor_name(spec):
    processors = dict(spec.predicates.iterall(what=b'.'))
    assert len(processors) == 1
    suffix = processors.keys()[0][1:]
    return specular.path_to_key(suffix)


@specular.make_constructor
def processor_constructor(spec, loc, top_spec, global_artifacts, settings):
    name = get_processor_name(spec) or loc[-1]
    read_keys = specular.getval(spec, ('read_keys',))
    write_keys = specular.getval(spec, ('write_keys',))

    action_loc = loc[:-2]
    action_name = action_loc[-1]
    factory_name = specular.getval(spec, ('module_path',))
    proc_artifacts = global_artifacts[factory_name]
    factory = utils.import_object(factory_name)

    collection_loc = action_loc[:-2]
    collection_values = proc_artifacts.get(collection_loc, {})

    action_values = proc_artifacts.get(action_loc, {})

    config_values = {}
    for conf_key, conf_value in settings.iteritems():
        value = conf_value if conf_value is not specular.ANY else None
        config_values[conf_key[1:]] = value

    arguments = dict(collection_values)
    arguments.update(action_values)
    arguments.update(config_values)
    proc = factory(collection_loc=collection_loc, action_name=action_name,
                   **arguments)
    return specular.Processor(name, reads=read_keys, writes=write_keys,
                              process=proc.process, cleanup=proc.cleanup)


@specular.make_constructor
def action_constructor(spec, loc, context, top_spec):
    action_name = loc[-1]
    assert loc[-2] == 'actions'
    collection_loc = loc[:-2]

    params = read_action_spec(spec)
    processors = list(specular.iter_spec_artifacts(context, ('processors',)))

    method = params['method']
    status_code = params['status_code']
    content_type = params['content_type']
    action_url = params['url']

    if method is None:
        msg = 'URL not found for action {!r}'.format(action_name)
        raise InvalidSpec(msg, loc=loc)
    if action_url is None:
        msg = 'HTTP method not found for action {!r}'.format(action_name)
        raise InvalidSpec(msg, loc=loc)

    logger.info("Constructing action: %s", action_name)
    collection_path = utils.mk_url_prefix(
        collection_loc, top_spec, wrapper=named_pattern)
    urlpattern = _construct_url(collection_path, action_url)
    method = method.upper()

    apimas_action = ApimasAction(
        collection_path, action_url, action_name, status_code, content_type,
        processors)
    return urlpattern, method, apimas_action


@specular.make_constructor
def endpoint_constructor(context):
    return {
        collection: mk_django_urls(collection_actions)
        for collection, collection_actions in specular.iter_spec_artifacts(
                context, ('collections',), keys=True)
    }


def mk_django_urls(action_urls):
    urls = []
    action_urls = sorted(action_urls.iteritems(), reverse=True)
    for urlpattern, method_actions in action_urls:
        django_view = django_views(method_actions)
        methods = method_actions.keys()
        http_methods = require_http_methods(methods)
        django_view = csrf_exempt(http_methods(django_view))
        urls.append(url(urlpattern, django_view))
    return urls


@specular.make_constructor
def apimas_app_constructor(context):
    urlpatterns = []
    for endpoint_patterns in specular.iter_spec_artifacts(
            context, ('endpoints',)):
        for collection, collection_patterns in endpoint_patterns.iteritems():
            urlpatterns.extend(collection_patterns)

    logger.info("Built URL patterns:")
    for urlpattern in urlpatterns:
        logger.info(urlpattern)
    return urlpatterns


REGISTERED_CONSTRUCTORS = {
    '.apimas_app': apimas_app_constructor,
    '.collection': collection_django_constructor,
    '.endpoint': endpoint_constructor,
    '.processor': processor_constructor,
    '.action': action_constructor,
}


def construct_processors(processors, spec):
    constructions = {}
    for processor in processors:
        constructors = utils.import_object(processor).Constructors
        constructions[processor] = constructors
    return spec.construct(constructions=constructions)


def configure_apimas_app(app_config):
    apimas_app_spec = domain.compile_spec({'.apimas_app': {}})
    return configure_spec(apimas_app_spec, app_config)


def configure_spec(spec, config):
    spec.config(config)
    return spec


def construct_views(spec):
    logger.info("Collecting processors...")
    processors = collect_processors(spec)
    artifacts = construct_processors(processors, spec)
    constructions = {'views': REGISTERED_CONSTRUCTORS}
    artifacts = spec.construct(
        constructions=constructions, artifacts=artifacts)
    return artifacts['views'][()]
