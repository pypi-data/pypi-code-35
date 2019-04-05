import specular
from django.db.models.query import QuerySet, Q
from apimas.base import ProcessorFactory
from apimas.errors import InvalidInput


@specular.make_constructor
def field_constructor(context, spec, output, loc):
    value = output or {}
    source = specular.getval(spec, ('source',), default=loc[-1])
    source = source.replace('.', '__')
    value['source'] = source
    return value


@specular.make_constructor
def searchable_constructor(output, loc):
    value = output or {}
    value['searchable'] = True
    return value


@specular.make_constructor
def collect_constructor(context, spec, output, loc):
    value = output or {}
    fields = {}

    for field_name, field_value in specular.iter_spec_artifacts(
            context, ('fields',), keys=True):

        if 'searchable' in field_value or field_value.get('fields'):
            fields[field_name] = field_value

    value['fields'] = fields
    return value


SEARCH_CONSTRUCTORS = {
    '.collection': collect_constructor,
    '.field.struct': collect_constructor,
    '.field': field_constructor,
    '.flag.searchable': searchable_constructor,
}


def collect_filters(fields, prefix):
    filters = []
    for key, spec in fields.iteritems():
        source = spec['source']
        path = prefix + (source,)
        if spec.get('searchable', False):
            filters.append('__'.join(path))

        subfields = spec.get('fields', {})
        filters.extend(collect_filters(subfields, path))
    return filters


def make_query(search_filters, value, operator='contains'):
    query = Q()
    for search_filter in search_filters:
        kwarg = {'%s__%s' % (search_filter, operator): value}
        query |= Q(**kwarg)
    return query


class Search(ProcessorFactory):
    Constructors = SEARCH_CONSTRUCTORS

    def __init__(self, collection_loc, action_name, fields, source=None):
        self.fields = fields
        self.search_filters = collect_filters(fields, ())

    def process(self, runtime_data):
        search_value = runtime_data['imported/search']
        queryset = runtime_data['backend/filtered_response']

        if not queryset or not search_value:
            return {}

        if not isinstance(queryset, QuerySet):
            msg = 'A queryset is expected, {!r} found'
            raise InvalidInput(msg.format(type(queryset)))

        search_query = make_query(self.search_filters, search_value)
        queryset = queryset.filter(search_query)
        queryset = queryset.distinct()
        return {'backend/filtered_response': queryset}
