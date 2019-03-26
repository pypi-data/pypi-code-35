from django.db import transaction
from .db import DatabaseContext
from .exceptions import AlreadyRegistered, DoesNotExist, RequestError
import json


class HandlerRegistry(object):
    def __init__(self):
        self.__handlers = {}

    def receive(self, source, request):
        try:
            handler = self.__handlers[source]
        except KeyError:
            raise DoesNotExist('Handler does not exist.')

        context = DatabaseContext()

        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            raise RequestError('Malformed JSON data')

        with transaction.atomic():
            response = handler(data, context)

        if response is None:
            return context.log()

    def register(self, name):
        def wrapper(func):
            if name in self.__handlers:
                raise AlreadyRegistered(
                    (
                        'A webhook handler with the name \'%s\' is '
                        'already reigstered'
                    ) % name
                )

            self.__handlers[name] = func

        return wrapper

    def unregister(self, name):
        try:
            del self.__handlers[name]
        except KeyError:
            raise DoesNotExist('Handler does not exist.')
