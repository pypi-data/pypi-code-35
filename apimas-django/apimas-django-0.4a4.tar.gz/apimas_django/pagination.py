from django.db.models.query import QuerySet
from apimas.base import ProcessorFactory
from apimas.errors import ValidationError, InvalidInput


class Pagination(ProcessorFactory):
    def __init__(
            self, collection_loc, action_name, pagination_default_limit=None):
        self.default_limit = pagination_default_limit

    def process(self, runtime_data):
        pagination_args = runtime_data['imported/pagination']
        queryset = runtime_data['backend/ordered_response']
        meta = runtime_data['exportable/meta'] or {}

        if not queryset or not pagination_args:
            return {'backend/selected_response': queryset,
                    'exportable/meta': meta}

        if not isinstance(queryset, QuerySet):
            msg = 'A queryset is expected, {!r} found'
            raise InvalidInput(msg.format(type(queryset)))

        offset, limit = pagination_args
        if limit is None:
            limit = self.default_limit

        if limit is None:
            raise ValidationError("'limit' parameter is required.")

        if offset is None:
            offset = 0

        begin, end = offset, offset + limit
        if not queryset.ordered:
           queryset = queryset.order_by('pk')
        else:
            # It seems that looking up queryset.ordered somehow interferes with
            # the slicing below, causing the queryset to be evaluated.
            # Create a new queryset to bypass that.
            queryset = queryset.filter()

        count = queryset.count()
        next_page = ''
        previous_page = ''
        queryset = queryset[begin:end]
        meta['count'] = count
        meta['next'] = next_page
        meta['previous'] = previous_page
        return {'backend/selected_response': queryset, 'exportable/meta': meta}
