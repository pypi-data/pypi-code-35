from django.test import TestCase
from .. import handlers
from ..exceptions import AlreadyRegistered, DoesNotExist


def test_handler(request):
    pass


class HandlerRegistryTests(TestCase):
    def test_register_unregister(self):
        handlers.register('test')(test_handler)

        with self.assertRaises(AlreadyRegistered):
            handlers.register('test')(test_handler)

        handlers.unregister('test')

        with self.assertRaises(DoesNotExist):
            handlers.unregister('test')
