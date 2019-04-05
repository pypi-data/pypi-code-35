from django.db.models  import Model
from django.db.models.query import QuerySet
from apimas.errors import InvalidInput
from apimas.base import ProcessorFactory
from apimas import utils
import specular


@specular.make_constructor
def construct_field(spec, loc):
    source = specular.getval(spec, ('source',), default=loc[-1])
    return {'source': source}


@specular.make_constructor
def construct_file(spec, loc, context):
    specular.construct_last(context)
    source = specular.getval(spec, ('source',), default=loc[-1])
    return {'source': source}


@specular.make_constructor
def construct_struct(spec, loc, context):
    specular.construct_last(context)
    source = specular.getval(spec, ('source',), default=loc[-1])
    fields = dict(specular.iter_spec_artifacts(
        context, ('fields',), keys=True))
    return {'source': source, 'fields': fields, 'field_type': 'struct'}


@specular.make_constructor
def construct_collection(spec, loc, context):
    specular.construct_last(context)
    source = specular.getval(spec, ('source',), default=loc[-1])
    fields = dict(specular.iter_spec_artifacts(
        context, ('fields',), keys=True))
    return {'source': source, 'fields': fields, 'field_type': 'collection'}


@specular.make_constructor
def construct_action(spec, loc):
    on_collection = specular.getval(spec, ('on_collection',))
    return {'on_collection': on_collection}


INSTANCETODICT_CONSTRUCTORS = {
    '.field': construct_field,
    '.field.struct': construct_struct,
    '.field.file': construct_file,
    '.action': construct_action,
    '.collection': construct_collection,
}


def access_relation(value, key):
    if hasattr(value, 'through'):
        flt = {value.source_field_name: key}
        return value.through.objects.filter(**flt)
    return value.all()


class InstanceToDict(ProcessorFactory):
    Constructors = INSTANCETODICT_CONSTRUCTORS

    def __init__(self, collection_loc, action_name,
                 source, fields, field_type, on_collection):
        self.collection_spec = {'source': source,
                                'fields': fields,
                                'field_type': field_type}
        self.on_collection = on_collection
        self.field_spec = fields

    def to_dict(self, instance, spec):
        if instance is None:
            return None

        data = {}
        for k, v in spec.iteritems():
            source = v['source'] if v else k
            fields = v.get('fields') if v else None
            fields_type = v.get('field_type') if v else None
            value = instance
            for elem in source.split('.'):
                if value is None:
                    break
                value = getattr(value, elem)

            if fields:
                if fields_type == 'collection':
                    subvalues = access_relation(value, key=instance)
                    value = [self.to_dict(subvalue, fields)
                             for subvalue in subvalues]
                elif fields_type == 'struct':
                    value = self.to_dict(value, fields)

            data[k] = value
        return data

    def process(self, processor_data):
        instance = processor_data['backend/checked_response']
        if instance is None:
            return {'exportable/content': None}

        if instance and (not isinstance(instance, Model) and not
                         isinstance(instance, QuerySet) and not
                         isinstance(instance, list)):
            msg = 'Unexpected type {!r} found.'
            raise InvalidInput(msg.format(type(instance)))

        if not self.on_collection:
            instance = None if instance is None else self.to_dict(
                instance, self.field_spec)
        else:
            instance = [self.to_dict(inst, self.field_spec)
                        for inst in instance]
        return {'exportable/content': instance}


class ResponseHandler(ProcessorFactory):
    def __init__(self, collection_loc, action_name, response_handler):
        if response_handler is None:
            raise InvalidInput("Must set ':response_handler'")
        self.response_handler = utils.import_object(response_handler)

    def process(self, data):
        response = data['backend/checked_response']
        runtime = data['$runtime']
        self.response_handler(response, runtime)
