import specular
from django.db.models.query import QuerySet
from apimas.base import ProcessorFactory
from apimas.errors import InvalidInput, AccessDeniedError


class Filter(object):

    def filter(self, queryset, source, operator, value):
        """
        Filter a given queryset based on a specific lookup operator, and a
        value.
        """
        operators = getattr(self, 'OPERATORS', [])
        if operator and operator not in operators:
            raise AccessDeniedError("No such operator")

        kwargs = {
            source + ('__' + operator if operator else ''): value
        }
        return queryset.filter(**kwargs)


class BooleanFilter(Filter):
    pass


class DateFilter(Filter):
    OPERATORS = (
        'gt',
        'gte',
        'lt',
        'lte',
        'range',
    )


class DateTimeFilter(DateFilter):
    pass


class StringFilter(Filter):
    OPERATORS = (
        'contains',
        'startswith',
        'endswith',
        'regex',
    )


class IntegerFilter(Filter):
    OPERATORS = (
        'gt',
        'gte',
        'lt',
        'lte',
    )


class FloatFilter(IntegerFilter):
    pass


@specular.make_constructor
def field_constructor(spec, output, loc):
    value = output or {}
    source = specular.getval(spec, ('source',), default=loc[-1])
    source = source.replace('.', '__')
    value['source'] = source
    return value


def filter_obj(cls):
    @specular.make_constructor
    def constructor(context, spec, output, loc):
        specular.construct_last(context)

        value = output or {}
        if value.get('filterable'):
            value['filter'] = cls()

        return value
    return constructor


def flag_constructor(flag):
    @specular.make_constructor
    def constructor(output, loc):
        value = output or {}
        value[flag] = True
        return value
    return constructor


@specular.make_constructor
def collect_constructor(context, spec, output, loc):
    field_filters = dict(specular.iter_spec_artifacts(
        context, ('fields',), keys=True))
    filters = {}
    for field_name, field_spec in field_filters.iteritems():
        if not field_spec:
            continue
        if 'filter' not in field_spec and 'filters' not in field_spec:
            continue
        filters[field_name] = field_spec

    value = output or {}
    value['filters'] = filters
    return value


FILTERING_CONSTRUCTORS = {
    '.collection': collect_constructor,
    '.field': field_constructor,
    '.field.struct': collect_constructor,
    '.field.string': filter_obj(StringFilter),
    '.field.serial': filter_obj(Filter),
    '.field.identity': filter_obj(Filter),
    '.field.ref': filter_obj(Filter),
    '.field.integer': filter_obj(IntegerFilter),
    '.field.float': filter_obj(FloatFilter),
    '.field.decimal': filter_obj(Filter),
    '.field.uuid': filter_obj(Filter),
    '.field.text': filter_obj(StringFilter),
    '.field.email': filter_obj(StringFilter),
    '.field.boolean': filter_obj(Filter),
    '.field.datetime': filter_obj(DateTimeFilter),
    '.field.date': filter_obj(DateFilter),
    '.field.choices': filter_obj(Filter),
    '.flag.filterable': flag_constructor('filterable'),
}



class Filtering(ProcessorFactory):
    """
    A django processor responsible for the filtering of a response, based
    on a query string.
    """
    Constructors = FILTERING_CONSTRUCTORS

    def __init__(self, collection_loc, action_name, filters, source=None):
        self.filters = filters

    def prepare_filter(self, filter_path):
        spec = {'filters': self.filters}
        source_path = []
        for segment in filter_path:
            spec = spec['filters']
            if segment not in spec:
                raise AccessDeniedError('%s not filterable (at %s)' %
                                        (str(filter_path), segment))
            spec = spec[segment]
            source_path.append(spec['source'])

        if 'filter' not in spec:
            raise AccessDeniedError('%s not filterable' % str(filter_path))
        return spec['filter'], '__'.join(source_path)

    def process(self, runtime_data):
        imported_filters = runtime_data['imported/filters']
        queryset = runtime_data['backend/filtered_response']

        if not queryset or not imported_filters:
            return {}

        if not isinstance(queryset, QuerySet):
            msg = 'A queryset is expected, {!r} found'
            raise InvalidInput(msg.format(type(queryset)))

        for filter_path, operator, value in imported_filters:
            filter_obj, source = self.prepare_filter(filter_path)
            queryset = filter_obj.filter(queryset, source, operator, value)

        queryset = queryset.distinct()
        return {'backend/filtered_response': queryset}
