import importlib
from urlparse import urljoin as urlparse_urljoin
import specular


def import_object(path):
    splits = path.rsplit('.', 1)
    if len(splits) != 2:
        raise ImportError("Malformed path")

    module_name, obj_name = splits
    module, trail = get_module(module_name)
    trail.append(obj_name)
    return import_prefixed_object(module, trail)


def get_module(module_name):
    trail = []
    name = module_name
    while True:
        try:
            mod = importlib.import_module(name)
            return mod, list(reversed(trail))
        except ImportError:
            splits = name.rsplit('.', 1)
            if len(splits) != 2:
                raise
            name = splits[0]
            trail.append(splits[1])


def import_prefixed_object(module, obj_elems):
    obj = module
    for elem in obj_elems:
        try:
            obj = getattr(obj, elem)
        except AttributeError:
            raise ImportError('Cannot import object {!r} from {!r}'.format(
                obj_elems, module))
    return obj


def urljoin(*urls):
    """ Constructs a URL based on multiple URL segments. """
    slash = '/'
    url = '/'
    for ufs in urls:
        url = urlparse_urljoin(url, ufs.strip(slash)).strip(slash) + slash
    return url


def mk_url_prefix(loc, top_spec, wrapper=None):
    endpoint_loc = tuple(loc[:2])
    endpoint_name = endpoint_loc[-1]
    endpoint_prefix_loc = endpoint_loc + ('prefix',)
    endpoint_prefix = specular.getval(
        top_spec, endpoint_prefix_loc, default=endpoint_name)
    segments = []
    collections = loc[3:]
    for i, name in enumerate(reversed(collections)):
        position, is_fields = divmod(i, 2)
        if not is_fields:
            segments.append(name)
        else:
            assert name == 'fields'
            if not wrapper:
                continue
            name = 'id' + str(position)
            segments.append(wrapper(name))
    segments.append(endpoint_prefix)
    return '/'.join(reversed(segments))
