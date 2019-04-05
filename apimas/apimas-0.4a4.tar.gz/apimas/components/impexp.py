import specular
from apimas import converters as cnvs
from apimas import documents as doc
from apimas.errors import AccessDeniedError, ValidationError, InvalidInput
from apimas.base import ProcessorFactory


Null = object()


def _converter_obj(cls, dependencies=None, extra_args=None):
    def constructor(context, spec, output, settings, loc, top_spec):
        specular.construct_last(context)
        output = output or {}
        kwargs = output.get('args', {})

        for key in dependencies or []:
            kwargs[key] = settings[':'+key]

        extra_check = extra_args or []
        for field_arg in extra_check:
            v = specular.getval(spec, (field_arg,), default=Null)
            if v is not Null:
                kwargs[field_arg] = v

        converter = cls(**kwargs)
        return {'converter': converter}
    return constructor


def converter_obj(cls, **kwargs):
    return specular.make_constructor(_converter_obj(cls, **kwargs))


def cerberus_flag(flag):
    @specular.make_constructor
    def constructor(output, loc):
        value = output or {}
        args = value.get('args', {})
        args[flag] = True
        value['args'] = args
        return value
    return constructor


@specular.make_constructor
def list_constructor(context, spec, output, settings, loc, top_spec):
    value = output or {}
    args = value.get('args', {})

    flat = specular.getval(spec, ('flat',), default=False)
    field_converters = dict(specular.iter_spec_artifacts(
        context, ('fields',), keys=True))
    resource_converter = cnvs.Struct(schema=field_converters, flat=flat)
    args['converter'] = resource_converter
    value['args'] = args

    return _converter_obj(cnvs.List, dependencies=None)(
        context, spec, value, settings, loc, top_spec)


@specular.make_constructor
def field_struct_constructor(context, spec, output, settings, loc, top_spec):
    value = output or {}
    args = value.get('args', {})

    field_converters = dict(specular.iter_spec_artifacts(
        context, ('fields',), keys=True))
    args['schema'] = field_converters
    value['args'] = args

    return _converter_obj(cnvs.Struct, dependencies=None)(
        context, spec, value, settings, loc, top_spec)


@specular.make_constructor
def construct_action(spec):
    on_collection = specular.getval(spec, ('on_collection',))
    return {'on_collection': on_collection}


IMPORTEXPORT_CONSTRUCTORS = {
    '.action': construct_action,
    '.collection': list_constructor,
    '.field.struct': field_struct_constructor,
    '.field.string': converter_obj(cnvs.String),
    '.field.serial': converter_obj(cnvs.Serial),
    '.field.identity': converter_obj(
        cnvs.Identity, dependencies=['root_url'], extra_args=['to']),
    '.field.ref': converter_obj(
        cnvs.Ref, dependencies=['root_url'], extra_args=['to']),
    '.field.integer': converter_obj(cnvs.Integer),
    '.field.float': converter_obj(cnvs.Float),
    '.field.decimal': converter_obj(
        cnvs.Decimal, dependencies=['decimal_places']),
    '.field.uuid': converter_obj(cnvs.UUID),
    '.field.text': converter_obj(cnvs.String),
    '.field.email': converter_obj(cnvs.Email),
    '.field.boolean': converter_obj(cnvs.Boolean),
    '.field.datetime': converter_obj(cnvs.DateTime),
    '.field.date': converter_obj(cnvs.Date),
    '.field.file': converter_obj(cnvs.File),
    '.field.choices': converter_obj(
        cnvs.Choices, extra_args=['allowed', 'displayed']),

    '.flag.noread': cerberus_flag('noread'),
    '.flag.nullable': cerberus_flag('nullable'),
}


class ImportExportData(ProcessorFactory):
    Constructors = IMPORTEXPORT_CONSTRUCTORS

    def __init__(self, collection_loc, action_name, converter, on_collection):
        self.on_collection = on_collection
        self.converter = converter if on_collection else converter.converter


def import_integer(value):
    return cnvs.Integer().import_data(value, permissions=True)


class ImportParams(ImportExportData):
    def __init__(self, collection_loc, action_name, filter_compat,
                 ordering_compat, **kwargs):
        self.filter_compat = bool(filter_compat)
        self.ordering_compat = bool(ordering_compat)
        ImportExportData.__init__(self, collection_loc, action_name, **kwargs)

    def process_filters(self, filters, can_read_fields, compat):
        filter_data = {}
        operators = {}
        for param, value in filters.iteritems():
            if compat:
                path = tuple(param.split('__'))
                operator = None
            else:
                parts = param.rsplit('__', 1)
                operator = parts[1] if len(parts) == 2 else None
                path = tuple(parts[0].split('.'))

            operators[path] = operator
            specular.doc_set(filter_data, path, value)

        converter = self.converter
        if self.on_collection:
            converter = converter.converter

        imported_filters = converter.import_data(
            filter_data, can_read_fields, single=True)

        result = []
        for path, operator in operators.iteritems():
            result.append(
                (path, operator, specular.doc_get(imported_filters, path)))
        return result

    def process_ordering(self, ordering_param, can_read_fields, compat):
        results = []
        orderings = ordering_param.split(',')
        for ordering in orderings:
            if ordering.startswith('-'):
                reverse = True
                ordering = ordering[1:]
            else:
                reverse = False

            separator = '__' if compat else '.'
            path = ordering.split(separator)
            if not specular.doc_get(can_read_fields, path):
                raise AccessDeniedError(
                    "You do not have permission to order by this field")
            results.append((path, reverse))
        return results

    def process_search(self, search_value):
        return cnvs.String().import_data(search_value, permissions=True)

    def process_parameters(self, runtime_data):
        parameters = runtime_data['request/meta/params']
        filters = {}
        ordering = None
        search = None
        pagination_offset = None
        pagination_limit = None
        for param, value in parameters.iteritems():
            if param == 'ordering':
                ordering = value
                continue

            if param == 'search':
                search = value
                continue

            if param == 'offset':
                pagination_offset = import_integer(value)
                continue

            if param == 'limit':
                pagination_limit = import_integer(value)
                continue

            if self.filter_compat:
                filters[param] = value
            else:
                parts = param.split('__', 1)
                if len(parts) != 2:
                    raise ValidationError(
                        "Unrecognized parameter '%s'" % param)
                if parts[0] == 'flt':
                    filters[parts[1]] = value
                else:
                    raise ValidationError(
                        "Unrecognized parameter '%s'" % param)

        read_fields = runtime_data['permissions/read/fields']
        result = {}
        if filters:
            result['imported/filters'] = self.process_filters(
                filters, read_fields, self.filter_compat)
        if ordering:
            result['imported/ordering'] = self.process_ordering(
                ordering, read_fields, self.ordering_compat)
        if search:
            result['imported/search'] = self.process_search(search)
        if pagination_offset is not None or pagination_limit is not None:
            result['imported/pagination'] = (
                pagination_offset, pagination_limit)

        return result

    def process(self, runtime_data):
        return self.process_parameters(runtime_data)


class ImportWriteData(ImportExportData):
    def process_write_data(self, runtime_data):
        write_data = runtime_data['request/content']
        can_write = runtime_data['permissions/write/enabled']
        if not can_write:
            raise AccessDeniedError(
                'You do not have permission to write to this resource')

        can_write_fields = runtime_data['permissions/write/fields']
        return self.converter.import_data(write_data, can_write_fields)

    def process(self, runtime_data):
        return {'imported/content': self.process_write_data(runtime_data)}


class ExportData(ImportExportData):
    """
    Processor responsible for the serialization of data.
    """
    def export_data(self, runtime_data):
        export_data = runtime_data['exportable/content']
        if export_data is None:
            return None
        can_read_fields = runtime_data['permissions/read/fields']
        exported_data = self.converter.export_data(
            export_data, can_read_fields, toplevel=True)
        if exported_data is cnvs.Nothing:
            return None
        return exported_data

    def process(self, runtime_data):
        exported = self.export_data(runtime_data)
        meta = runtime_data['exportable/meta']
        if not meta:
            response = exported
        else:
            if 'results' in meta:
                raise InvalidInput("Conflicting key 'results' in meta")
            response = dict(meta)
            response['results'] = exported

        return {'response/content': response}
