from django.db import models
from django.db.models.query import QuerySet
from apimas_django.handlers import get_model_instance, DjangoProcessorFactory
from apimas.base import ProcessorFactory
from apimas.errors import NotFound


def filter_collection(queryset, filter_func, runtime):
    flt = filter_func(runtime)
    return queryset.filter(flt)


def filter_resource(spec, pk, kwargs, filter_func, runtime, strict):
    flt = filter_func(runtime)
    try:
        return get_model_instance(spec, pk, kwargs, filters=[flt])
    except NotFound:
        if strict:
            raise
        return None


class FilterResourceResponse(DjangoProcessorFactory):
    def __init__(self, collection_loc, action_name, spec,
                 filter_resource_strict):
        self.collection_loc = collection_loc
        self.collection_name = collection_loc[-1]
        self.spec = spec
        self.strict = bool(filter_resource_strict)

    def process(self, runtime_data):
        runtime = runtime_data['$runtime']
        unfiltered_response = runtime_data['backend/raw_response']
        kwargs = runtime_data['request/meta/kwargs']
        read_filter = runtime_data['permissions/read/filter']

        if read_filter is None:
            filtered_response = unfiltered_response
        else:
            assert isinstance(unfiltered_response, models.Model)
            pk = unfiltered_response.pk
            filtered_response = filter_resource(
                self.spec, pk, kwargs, read_filter, runtime, self.strict)

        return {'backend/filtered_response': filtered_response}


class ObjectRetrievalForUpdate(DjangoProcessorFactory):
    def process(self, runtime_data):
        runtime = runtime_data['$runtime']
        kwargs = runtime_data['request/meta/kwargs']
        pk = kwargs['pk']
        write_filter = runtime_data['permissions/write/filter']
        filters = []
        if write_filter is not None:
            filters.append(write_filter(runtime))

        instance = get_model_instance(self.spec, pk, kwargs, filters,
                                      for_update=True)
        return {'backend/instance': instance}


class FilterCollectionResponse(DjangoProcessorFactory):
    def __init__(self, collection_loc, action_name, spec):
        self.collection_loc = collection_loc
        self.collection_name = collection_loc[-1]
        self.spec = spec

    def process(self, runtime_data):
        runtime = runtime_data['$runtime']
        unfiltered_response = runtime_data['backend/raw_response']
        read_filter = runtime_data['permissions/read/filter']

        if read_filter is None:
            filtered_response = unfiltered_response
        else:
            assert isinstance(unfiltered_response, QuerySet)
            filtered_response = filter_collection(
                unfiltered_response, read_filter, runtime)

        return {'backend/filtered_response': filtered_response}


class WritePermissionCheck(ProcessorFactory):
    def process(self, runtime_data):
        runtime = runtime_data['$runtime']
        backend_input = runtime_data['backend/input']
        instance = runtime_data.get('backend/instance')
        write_check = runtime_data['permissions/write/check']

        if write_check is None:
            return {}

        write_check(backend_input, instance, runtime)
        return {'guards/write_check': True}


class ReadPermissionCheck(ProcessorFactory):
    def __init__(self, collection_loc, action_name, read_check_strict):
        self.collection_loc = collection_loc
        self.action_name = action_name
        self.strict = bool(read_check_strict)

    def process(self, runtime_data):
        runtime = runtime_data['$runtime']
        unchecked_response = runtime_data['backend/selected_response']
        read_check = runtime_data['permissions/read/check']

        if read_check is None or unchecked_response is None:
            checked_response = unchecked_response
            return {'backend/checked_response': checked_response}

        checked_response = read_check(unchecked_response, runtime)
        if checked_response is None and self.strict:
            raise NotFound("Resource not found")

        return {'backend/checked_response': checked_response}


class AssumeChecked(ProcessorFactory):
    def process(self, runtime_data):
        raw = runtime_data['backend/raw_response']
        return {'backend/checked_response': raw}


class FilteredAsSelected(ProcessorFactory):
    def process(self, runtime_data):
        raw = runtime_data['backend/filtered_response']
        return {'backend/selected_response': raw}
