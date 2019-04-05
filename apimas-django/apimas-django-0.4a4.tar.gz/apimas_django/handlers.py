import logging
from django.db.models import ProtectedError
from django.db import transaction, IntegrityError
from apimas import utils
from apimas_django import utils as django_utils
from apimas.base import ProcessorFactory
from apimas.errors import AccessDeniedError, InvalidInput, ConflictError
import specular

logger = logging.getLogger('apimas')

REF = '.ref'
STRUCT = '.struct='
ARRAY_OF = '.array of='

Nothing = type('Nothing', (), {'__repr__': lambda self: 'Nothing'})()


def get_bounds(loc, top_spec):
    bounds = []
    working_loc = loc
    while len(working_loc) >= 2:
        bound = specular.getval(
            top_spec, working_loc + ('bound',), default=None)
        if bound is None:
            break
        bounds.append(bound)
        working_loc = working_loc[:-2]
    return bounds


def get_sub_elements(instance, context):
    subcollections = {}
    substructs = {}
    subfields = {}
    for field, field_value in specular.iter_spec_artifacts(
            context, ('fields',), keys=True):
        if field_value:
            field_spec = field_value['spec']
            field_type = field_spec['type']
            if field_type == 'collection':
                subcollections[field] = field_spec
            elif field_type == 'struct':
                substructs[field] = field_spec
            elif field_type == 'regular':
                subfields[field] = field_spec
    return subcollections, substructs, subfields


@specular.make_constructor
def struct_constructor(context, spec, loc, output):
    specular.construct_last(context)
    value = output
    value_spec = value['spec']

    source = specular.getval(spec, ('source',), default=loc[-1])
    subcollections, substructs, subfields = get_sub_elements(
        spec, context)
    value_spec['type'] = 'struct'
    value_spec['source'] = source
    value_spec['subcollections'] = subcollections
    value_spec['substructs'] = substructs
    value_spec['subfields'] = subfields
    return value


@specular.make_constructor
def collection_constructor(context, spec, loc, output, top_spec):
    specular.construct_last(context)
    value = output or {}
    value_spec = value.get('spec', {})

    model = specular.getval(spec, ('model',))
    source = specular.getval(spec, ('source',), default=None)
    id_field = specular.getval(spec, ('id_field',), default='id')

    subset = specular.getval(spec, ('subset',), default=None)
    bounds = get_bounds(loc, top_spec)
    subcollections, substructs, subfields = get_sub_elements(
        spec, context)

    if id_field not in subfields:
        raise InvalidInput("'id_field' not specified as field")

    id_field_spec = subfields[id_field]
    db_key = id_field_spec['source']

    value_spec['type'] = 'collection'
    value_spec['model'] = utils.import_object(model)
    value_spec['source'] = source
    value_spec['id_field'] = id_field
    value_spec['db_key'] = db_key
    value_spec['subset'] = utils.import_object(subset) if subset else None
    value_spec['bounds'] = bounds
    value_spec['subcollections'] = subcollections
    value_spec['substructs'] = substructs
    value_spec['subfields'] = subfields
    value['spec'] = value_spec
    return value


@specular.make_constructor
def field_constructor(spec, loc, output):
    value = output or {}
    value_spec = value.get('spec', {})
    value_spec['type'] = 'regular'
    source = specular.getval(spec, ('source',), default=loc[-1])
    value_spec['source'] = source

    def_doc = specular.getval(spec, ('default',), default=Nothing)
    deffn_doc = specular.getval(
        spec, ('default_fn',), default=Nothing)

    if def_doc is not Nothing and deffn_doc is not Nothing:
        raise InvalidInput("Multiple default values given")

    if def_doc is not Nothing:
        value_spec['default'] = lambda: def_doc
    elif deffn_doc is not Nothing:
        fn = utils.import_object(deffn_doc)
        value_spec['default'] = fn

    value['spec'] = value_spec
    return value


def construct_flag(flag):
    @specular.make_constructor
    def constructor(output, loc):
        value = output or {}
        spec = value.get('spec', {})
        flags = spec.get('flags', [])
        flags.append(flag)
        spec['flags'] = flags
        value['spec'] = spec
        return value
    return constructor


DJANGOBASEHANDLER_CONSTRUCTORS = {
    '.field': field_constructor,
    '.field.struct': struct_constructor,
    '.collection': collection_constructor,
    '.flag.nowrite': construct_flag('nowrite'),
    '.flag.noread': construct_flag('noread'),
    '.flag.noupdate': construct_flag('noupdate'),
    '.flag.nullable': construct_flag('nullable'),
}


class DjangoProcessorFactory(ProcessorFactory):
    """
    Base handler for django specific actions.
    """
    Constructors = DJANGOBASEHANDLER_CONSTRUCTORS

    def __init__(self, collection_loc, action_name, spec):
        self.collection_loc = collection_loc
        self.collection_name = collection_loc[-1]
        self.spec = spec


def get_fields(subspecs, data):
    create_args = {}
    for field_name, field_spec in subspecs.iteritems():
        source = field_spec['source']
        value = data.get(source, Nothing)
        if value is not Nothing:
            create_args[source] = value

    return create_args


def get_bound_name(spec):
    bounds = spec.get('bounds')
    if bounds:
        bound = bounds[0]
        return bound + '_id'
    return None


def model_create_fn(model):
    try:
        return getattr(model, 'apimas_create')
    except AttributeError:
        return model.objects.create


def standard_update(instance, update_args):
    for key, value in update_args.iteritems():
        setattr(instance, key, value)
    instance.save()


def model_update_fn(model):
    try:
        return getattr(model, 'apimas_update')
    except AttributeError:
        return standard_update


def do_create(key, spec, data, precreated=None):
    create_args = {}
    if precreated:
        create_args.update(precreated)

    model = spec['model']
    bound_name = get_bound_name(spec)
    if bound_name is not None:
        assert key
        create_args[bound_name] = key

    create_args.update(get_fields(spec['subfields'], data))

    logger.debug('Creating values: %s', create_args)
    try:
        return model_create_fn(model)(**create_args)
    except IntegrityError as exc:
        msg = 'UNIQUE constraint failed'
        if msg in exc.message:
            raise ConflictError(msg)
        raise


def defer_create_subcollections(spec, data):
    deferred = []
    for subname, subspec in spec['subcollections'].iteritems():
        subsource = subspec['source']
        subdata = data.get(subsource, Nothing)
        if subdata is Nothing:
            continue
        deferred.extend((subspec, elem) for elem in subdata)
    return deferred


def create_substructs(spec, data):
    created = {}
    model = spec['model']
    for subname, subspec in spec['substructs'].iteritems():
        subsource = subspec['source']
        field = model._meta.get_field(subsource)
        struct_model = field.related_model
        subspec['model'] = struct_model
        subdata = data.get(subsource, Nothing)
        struct_instance = create_resource(subspec, subdata)
        if struct_instance is not Nothing:
            created[subsource] = struct_instance
    return created


def create_resource(spec, data, key=None):
    if data is Nothing:
        return Nothing

    if data is None:
        return None

    deferred = defer_create_subcollections(spec, data)
    precreated = create_substructs(spec, data)
    instance = do_create(key, spec, data, precreated)
    for args in deferred:
        create_resource(*args, key=instance.pk)
    return instance


def delete_subcollection(key, spec):
    model = spec['model']
    bound_name = get_bound_name(spec)
    assert bound_name is not None
    flt = {bound_name: key}
    logger.debug('Deleting with filter: %s', flt)
    delete_queryset(model.objects.filter(**flt))


def update_subcollections(spec, data, instance):
    for subname, subspec in spec['subcollections'].iteritems():
        subsource = subspec['source']
        subdata = data.get(subsource, Nothing)
        if subdata is Nothing:
            continue
        delete_subcollection(instance.pk, subspec)
        for elem in subdata:
            create_resource(subspec, elem, key=instance.pk)


def update_substructs(spec, data, instance):
    created = {}
    model = spec['model']
    for subname, subspec in spec['substructs'].iteritems():
        subsource = subspec['source']
        field = model._meta.get_field(subsource)
        struct_model = field.related_model
        subspec['model'] = struct_model
        subdata = data.get(subsource, Nothing)
        subinstance = getattr(instance, subsource)
        if subinstance is None:
            struct_instance = create_resource(subspec, subdata)
            if struct_instance is not Nothing:
                created[subsource] = struct_instance
        else:
            struct_instance = update_resource(subspec, subdata, subinstance)
            if struct_instance is None:
                created[subsource] = None
    return created


def do_update(spec, data, instance, precreated=None):
    update_args = {}
    if precreated:
        update_args.update(precreated)

    update_args.update(get_fields(spec['subfields'], data))

    logger.debug('Updating values: %s', update_args)
    model = spec['model']
    try:
        model_update_fn(model)(instance, update_args)
    except IntegrityError as exc:
        msg = 'UNIQUE constraint failed'
        if msg in exc.message:
            raise ConflictError(msg)
        raise
    return instance


def update_resource(spec, data, instance):
    if data is Nothing:
        return Nothing

    if data is None:
        logger.debug('Deleting instance: %s', instance)
        delete_instance(instance)
        return None

    update_subcollections(spec, data, instance)
    precreated = update_substructs(spec, data, instance)
    return do_update(spec, data, instance, precreated)


def delete_instance(instance):
    try:
        instance.delete()
    except ProtectedError:
        raise AccessDeniedError('Deleting this resource is forbidden')


def delete_queryset(queryset):
    try:
        queryset.delete()
    except ProtectedError:
        raise AccessDeniedError('Deleting these resources is forbidden')


class CreateHandler(DjangoProcessorFactory):
    def __init__(self, custom_create_handler, **kwargs):
        self.custom_create_handler = utils.import_object(
            custom_create_handler) if custom_create_handler else None
        DjangoProcessorFactory.__init__(self, **kwargs)

    def process(self, runtime_data):
        """ Creates a new django model instance. """

        runtime = runtime_data['$runtime']
        data = runtime_data['backend/input']
        kwargs = runtime_data['request/meta/kwargs']
        key = kwargs.get('id0')

        if self.custom_create_handler:
            instance = self.custom_create_handler(
                data, key, runtime)
        else:
            instance = create_resource(self.spec, data, key=key)

        if self.spec['subset']:
            instance = get_model_instance(
                self.spec, instance.pk, kwargs, strict=False)
        return {'backend/raw_response': instance}


def select_related(objects, substructs):
    for key, value in substructs.iteritems():
        source = value['source']
        if source:
            objects = objects.select_related(source)
    return objects


def prefetch_related(objects, subcollections):
    for key, value in subcollections.iteritems():
        source = value['source']
        if source:
            objects = objects.prefetch_related(source)
    return objects


def get_bound_filters(bounds, kwargs):
    flts = {}
    prev = ''
    for i, bound in enumerate(bounds):
        prefix = (prev + '__') if prev else ''
        ref = prefix + bound
        flts[ref + '_id'] = kwargs['id' + str(i)]
        prev = ref
    return flts


class ListHandler(DjangoProcessorFactory):
    def process(self, runtime_data):
        """
        Gets all django model instances based on the orm model extracted
        from request runtime.
        """
        kwargs = runtime_data['request/meta/kwargs']
        return {'backend/raw_response': get_collection_objects(self.spec, kwargs)}


def get_collection_objects(spec, bounds):
    model = spec['model']
    subset = spec['subset']
    bound_filters = get_bound_filters(spec['bounds'], bounds)
    objects = model.objects.filter(**bound_filters)
    if subset:
        objects = objects.filter(subset)
    objects = prefetch_related(objects, spec['subcollections'])
    objects = select_related(objects, spec['substructs'])
    return objects


def running_in_transaction():
    return not transaction.get_autocommit()


def get_model_instance(spec, pk, kwargs, filters=None, strict=True,
                       for_update=False):
    db_key = spec['db_key']
    objects = get_collection_objects(spec, kwargs)
    if filters:
        objects = objects.filter(*filters)
    if for_update and running_in_transaction():
        objects = objects.select_for_update()
    return django_utils.get_instance(
        objects, pk, pk_name=db_key, strict=strict)


class RetrieveHandler(DjangoProcessorFactory):
    def process(self, runtime_data):
        """
        Gets a single model instance which based on the orm model and
        resource ID extracted from request runtime.
        """
        kwargs = runtime_data['request/meta/kwargs']
        pk = kwargs['pk']
        instance = get_model_instance(self.spec, pk, kwargs)
        return {'backend/raw_response': instance}


class UpdateHandler(DjangoProcessorFactory):
    def __init__(self, custom_update_handler, **kwargs):
        self.custom_update_handler = utils.import_object(
            custom_update_handler) if custom_update_handler else None
        DjangoProcessorFactory.__init__(self, **kwargs)

    def process(self, runtime_data):
        """
        Updates an existing model instance based on the data of request.
        """
        runtime = runtime_data['$runtime']
        kwargs = runtime_data['request/meta/kwargs']
        pk = kwargs['pk']
        data = runtime_data['backend/input']
        instance = runtime_data['backend/instance']
        if not instance:
            instance = get_model_instance(self.spec, pk, kwargs,
                                          for_update=True)

        if self.custom_update_handler:
            self.custom_update_handler(data, instance, runtime)
        else:
            update_resource(self.spec, data, instance)

        instance = get_model_instance(self.spec, pk, kwargs, strict=False)
        return {'backend/raw_response': instance}


class DeleteHandler(RetrieveHandler):
    def process(self, runtime_data):
        """ Deletes an existing model instance. """
        write_data = RetrieveHandler.process(
            self, runtime_data)
        instance = write_data['backend/raw_response']
        delete_instance(instance)
        return {'backend/raw_response': None}
