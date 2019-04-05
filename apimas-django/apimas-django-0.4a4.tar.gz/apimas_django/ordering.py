import specular
from django.db.models.query import QuerySet
from apimas.base import ProcessorFactory
from apimas.errors import InvalidInput, AccessDeniedError


@specular.make_constructor
def field_constructor(context, spec, output, loc):
    specular.construct_last(context)
    value = output or {}
    source = specular.getval(spec, ('source',), default=loc[-1])
    source = source.replace('.', '__')
    value['source'] = source
    return value


def flag_constructor(flag):
    @specular.make_constructor
    def constructor(output, loc):
        value = output or {}
        value[flag] = True
        return value
    return constructor


@specular.make_constructor
def collect_constructor(context, spec, output, loc):
    field_data = dict(specular.iter_spec_artifacts(
        context, ('fields',), keys=True))
    value = output or {}
    propagate_fields = {}
    for field_name, field_spec in field_data.iteritems():
        if not field_spec:
            continue
        if 'orderable' not in field_spec and 'fields' not in field_spec:
            continue
        propagate_fields[field_name] = field_spec

    value['fields'] = propagate_fields
    return value


ORDERING_CONSTRUCTORS = {
    '.collection': collect_constructor,
    '.field.struct': collect_constructor,
    '.field': field_constructor,
    '.flag.orderable': flag_constructor('orderable'),
}


class Ordering(ProcessorFactory):
    Constructors = ORDERING_CONSTRUCTORS

    def __init__(self, collection_loc, action_name, fields, source=None):
        self.fields = fields

    def get_ordering_source(self, ordering_path):
        spec = {'fields': self.fields}
        source_path = []
        for segment in ordering_path:
            spec = spec['fields']
            if segment not in spec:
                raise AccessDeniedError('%s not orderable (at %s)' %
                                        (str(ordering_path), segment))
            spec = spec[segment]
            source_path.append(spec['source'])

        if 'orderable' not in spec:
            raise AccessDeniedError('%s not orderable' % str(ordering_path))
        return '__'.join(source_path)

    def process(self, runtime_data):
        imported_ordering = runtime_data['imported/ordering']
        queryset = runtime_data['backend/filtered_response']

        if not queryset or not imported_ordering:
            return {'backend/ordered_response': queryset}

        if not isinstance(queryset, QuerySet):
            msg = 'A queryset is expected, {!r} found'
            raise InvalidInput(msg.format(type(queryset)))

        orderings = []
        for ordering_path, reverse in imported_ordering:
            source = self.get_ordering_source(ordering_path)
            orderings.append('%s%s' % ('-' if reverse else '', source))

        # Ensure we always have a total order
        orderings.append('pk')

        if orderings:
            queryset = queryset.order_by(*orderings)
        return {'backend/ordered_response': queryset}
